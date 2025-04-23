import os
import asyncio
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from atproto import Client as BlueskyClient
import pandas as pd
import time
from dotenv import load_dotenv
import logging
import re
from datetime import datetime, timedelta
import redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BLUE_SKY_HANDLE = os.getenv('BLUE_SKY_HANDLE')
BLUE_SKY_APP_PASSWORD = os.getenv('BLUE_SKY_APP_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Validate environment variables
if not all([BLUE_SKY_HANDLE, BLUE_SKY_APP_PASSWORD, OPENAI_API_KEY]):
    logger.error("Missing required environment variables!")
    logger.debug(f"BLUE_SKY_HANDLE: {'Set' if BLUE_SKY_HANDLE else 'Not Set'}")
    logger.debug(f"BLUE_SKY_APP_PASSWORD: {'Set' if BLUE_SKY_APP_PASSWORD else 'Not Set'}")
    logger.debug(f"OPENAI_API_KEY: {'Set' if OPENAI_API_KEY else 'Not Set'}")
    raise ValueError("Missing required environment variables!")

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize Redis for caching
redis_client = redis.from_url(REDIS_URL)

# Initialize Bluesky client and authenticate
bs_client = BlueskyClient()

def validate_bluesky_handle(handle):
    """Validate Bluesky handle format."""
    pattern = r'^[a-zA-Z0-9._-]+\.bsky\.social$'
    return bool(re.match(pattern, handle))

def cache_key(handle):
    """Generate cache key for a Bluesky handle."""
    return f"bluesky_posts:{handle}"

def get_cached_posts(handle):
    """Get cached posts for a handle."""
    key = cache_key(handle)
    cached = redis_client.get(key)
    if cached:
        return eval(cached)
    return None

def cache_posts(handle, posts, expiry=3600):
    """Cache posts for a handle."""
    key = cache_key(handle)
    redis_client.setex(key, expiry, str(posts))

def authenticate_bluesky():
    """Authenticate with Bluesky."""
    try:
        bs_client.login(
            login=BLUE_SKY_HANDLE,
            password=BLUE_SKY_APP_PASSWORD
        )
        logger.info(f"Successfully authenticated as {BLUE_SKY_HANDLE}")
    except Exception as e:
        logger.error(f"Bluesky authentication failed: {str(e)}")
        raise


# Prompt template for classification
PROMPT_TEMPLATE = (
    "You are an AI trained to classify political statements according to three clearly defined ideological dimensions.\n\n"
    "Please analyze the following statement and provide a classification score for each axis on a scale from -1.00 to 1.00, with **two decimal places** of precision.\n\n"
    "Definitions of each dimension:\n"
    "1. **Economic Policy [-1.00 to 1.00]**\n"
    "   - -1.00 = Strongly supports government intervention, wealth redistribution, or socialism.\n"
    "   -  0.00 = Balanced or mixed economy.\n"
    "   -  1.00 = Strongly supports free markets, privatization, or laissez-faire capitalism.\n\n"
    "2. **Social Values [-1.00 to 1.00]**\n"
    "   - -1.00 = Strongly progressive, liberal, or pro-diversity (e.g., supports minority rights, secularism).\n"
    "   -  0.00 = Moderate or centrist on social issues.\n"
    "   -  1.00 = Strongly conservative, traditionalist, or religious (e.g., favors traditional family, national identity).\n\n"
    "3. **Government Structure [-1.00 to 1.00]**\n"
    "   - -1.00 = Strongly favors decentralization, direct democracy, or anarchism.\n"
    "   -  0.00 = Supports a balance of central and local governance.\n"
    "   -  1.00 = Strongly favors centralized authority, authoritarianism, or technocracy.\n\n"
    "Output format: [Economic Policy, Social Values, Government Structure]\n"
    "Ensure the result is strictly numeric in the format of: [-0.87, 0.22, -0.56]\n\n"
    "Statement:\n\"{}\"\n"
)

def classify_texts(texts):
    """Classify texts using OpenAI API with rate limiting and error handling."""
    results = []
    for text in texts:
        try:
            prompt = PROMPT_TEMPLATE.format(text)
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            output = resp.choices[0].message.content.strip()
            try:
                scores = eval(output)
                if isinstance(scores, list) and len(scores) == 3:
                    results.append({
                        "text": text,
                        "scores": {
                            "Economic Policy": scores[0],
                            "Social Value": scores[1],
                            "Government Structure": scores[2]
                        }
                    })
            except Exception as e:
                logger.error(f"Error parsing classification output: {str(e)}")
                continue
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            logger.error(f"Error in classification: {str(e)}")
            continue
    return results

@app.route('/full_pipeline', methods=['POST'])
@limiter.limit("10 per minute")
def full_pipeline():
    """Main pipeline endpoint with error handling and caching."""
    try:
        data = request.get_json(force=True)
        user_input = data.get("userInput")
        
        if not user_input:
            return jsonify({"error": "userInput is required"}), 400
            
        if not validate_bluesky_handle(user_input):
            return jsonify({"error": "Invalid Bluesky handle format"}), 400

        # Check cache first
        cached_posts = get_cached_posts(user_input)
        if cached_posts:
            return jsonify(cached_posts)

        # Authenticate with Bluesky
        try:
            authenticate_bluesky()
        except Exception as e:
            logger.exception(f"Bluesky authentication failed: {str(e)}")
            return jsonify({"error": "Failed to authenticate with Bluesky"}), 500

        # Fetch BlueSky posts
        try:
            logger.debug(f"Attempting to fetch posts for user: {user_input}")
            resp = bs_client.app.bsky.feed.get_author_feed(params={
                "actor": user_input,
                "limit": 25
            })
            feed = resp.feed
            logger.debug(f"Successfully fetched {len(feed) if feed else 0} posts")
        except Exception as e:
            logger.exception(f"Bluesky fetch failed with detailed error: {str(e)}")
            return jsonify({
                "error": "Failed to fetch Bluesky posts",
                "details": str(e),
                "type": type(e).__name__
            }), 500

        texts = [
            item.post.record.text
            for item in feed
            if getattr(item, "post", None) and getattr(item.post, "record", None) and item.post.record.text
        ]
        
        if not texts:
            logger.warning(f"No valid posts found for user: {user_input}")
            return jsonify({"error": "No posts found"}), 404

        # Classification
        results = classify_texts(texts)
        if not results:
            return jsonify({"error": "Classification failed"}), 500

        # Compute averages
        df = pd.DataFrame([r["scores"] for r in results])
        averages = df.mean().round(2).to_dict()

        response_data = {
            "results": results,
            "average": averages
        }
        
        # Cache the results
        cache_posts(user_input, response_data)
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
