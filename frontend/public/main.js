// main.js

document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    const userInput = document.getElementById('userInput');
    const resultContainer = document.getElementById('resultContainer');
    let isProcessing = false;

    // Add loading state styles
    const style = document.createElement('style');
    style.textContent = `
        .loading {
            opacity: 0.5;
            pointer-events: none;
        }
        .error {
            color: #dc3545;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #dc3545;
            border-radius: 4px;
            background-color: #f8d7da;
        }
        .success {
            color: #28a745;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #28a745;
            border-radius: 4px;
            background-color: #d4edda;
        }
    `;
    document.head.appendChild(style);

    function setLoading(isLoading) {
        isProcessing = isLoading;
        submitBtn.disabled = isLoading;
        userInput.disabled = isLoading;
        submitBtn.textContent = isLoading ? 'Processing...' : 'Submit';
        if (isLoading) {
            submitBtn.classList.add('loading');
        } else {
            submitBtn.classList.remove('loading');
        }
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        resultContainer.innerHTML = '';
        resultContainer.appendChild(errorDiv);
    }

    function showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success';
        successDiv.textContent = message;
        resultContainer.innerHTML = '';
        resultContainer.appendChild(successDiv);
    }

    function validateInput(input) {
        const pattern = /^[a-zA-Z0-9._-]+\.bsky\.social$/;
        if (!pattern.test(input)) {
            return 'Please enter a valid Bluesky handle (e.g., username.bsky.social)';
        }
        return null;
    }

    async function fetchPosts(handle) {
        try {
            const response = await fetch('http://localhost:5001/full_pipeline', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ userInput: handle })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            throw error;
        }
    }

    function displayResults(data) {
        resultContainer.innerHTML = '';
        
        // Display average scores
        const avgDiv = document.createElement('div');
        avgDiv.className = 'averages';
        avgDiv.innerHTML = `
            <h3>Average Scores</h3>
            <ul>
                <li>Economic Policy: ${data.average["Economic Policy"]}</li>
                <li>Social Value: ${data.average["Social Value"]}</li>
                <li>Government Structure: ${data.average["Government Structure"]}</li>
            </ul>
        `;
        resultContainer.appendChild(avgDiv);

        // Display individual posts
        data.results.forEach(item => {
            const postEl = document.createElement('div');
            postEl.className = 'post';
            postEl.innerHTML = `
                <p><strong>Text:</strong> ${item.text}</p>
                <p><em>Scores: [${item.scores["Economic Policy"]}, ${item.scores["Social Value"]}, ${item.scores["Government Structure"]}]</em></p>
                <hr/>
            `;
            resultContainer.appendChild(postEl);
        });
    }

    submitBtn.addEventListener('click', async () => {
        if (isProcessing) return;

        const handle = userInput.value.trim();
        const validationError = validateInput(handle);
        
        if (validationError) {
            showError(validationError);
            return;
        }

        setLoading(true);
        try {
            const data = await fetchPosts(handle);
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
        } finally {
            setLoading(false);
        }
    });

    // Add enter key support
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !isProcessing) {
            submitBtn.click();
        }
    });
});
  