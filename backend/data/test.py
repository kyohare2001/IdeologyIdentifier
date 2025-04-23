from openai import OpenAI
import os
import pandas as pd
import matplotlib.pyplot as plt
import time
from dotenv import load_dotenv

load_dotenv()
#openai.api_key = os.environ.get("OPEN_AI_API_KEY")

client = OpenAI(
  organization='org-ZHTkxU9gaXuC5oVEzwTEOPD5',
  project='',
  api_key = os.environ.get('OPEN_AI_API_KEY') # environ でapi.mdに書いた内容を取得
)

# 分類対象のテキスト
text_input = "When politicians say 'we can't afford it,' ask them who 'we' is. Because billionaires just got another tax break."

# プロンプト（システムメッセージが使えないモデル向けに、全てユーザーメッセージに統合）
userContent = (
    "You are an AI trained to classify political statements based on three key ideological dimensions:\n\n"
    "1. Economic Policy (-1.00 to 1.00): Measures support for government intervention in the economy.\n"
    "   - -1: Strongly favors free-market capitalism and minimal government regulation.\n"
    "   - 0: Neutral or mixed stance on government intervention.\n"
    "   - 1: Strongly favors government control, welfare policies, or socialism.\n\n"
    "2. Social Value (-1.00 to 1.00): Measures stance on progressive vs. conservative social policies.\n"
    "   - -1: Highly conservative (e.g., opposes LGBTQ rights, supports traditional values).\n"
    "   - 0: Neutral or balanced view on social issues.\n"
    "   - 1: Highly progressive (e.g., supports gender equality, LGBTQ rights, liberal immigration policies).\n\n"
    "3. Government Structure (-1.00 to 1.00): Measures preference for centralized vs. decentralized governance.\n"
    "   - -1: Prefers small government, libertarianism, or limited federal power.\n"
    "   - 0: Neutral or pragmatic stance on government size.\n"
    "   - 1: Prefers strong government, federal control, or centralized authority.\n\n"
    "Examples:\n"
    "1. \"The government should raise taxes to fund universal healthcare.\" → [0.79, 0.45, -0.19]\n"
    "2. \"The economy works best when businesses are free from government interference.\" → [-0.92, 0.11, -0.70]\n"
    "3. \"Gun control laws should be stricter to ensure public safety.\" → [0.20, 0.88, 0.13]\n"
    "4. \"States should have more autonomy to decide on education policies, not the federal government.\" → [0.31, -0.20, -0.80]\n\n"
    "Please classify the following statement according to these three dimensions and return the results in the exact format "
    "[Economic Policy, Social Value, Government Structure] as continuous values formatted to two decimal places.\n\n"
    "Statement:\n\"{}\"\n\n"
    "Output format: [Economic Policy, Social Value, Government Structure]"
).format(text_input)

results = []

# API呼び出しを100回実施して結果をリストに格納
for i in range(100):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # 使用するモデルを指定（モデル名が正しいか確認してください）
        messages=[
            {"role": "user", "content": userContent}
        ],
        temperature=0  # 安定した出力のため temperature=0
    )
    output = response.choices[0].message.content.strip()
    try:
        # 出力例: "[0.60, 0.80, -0.10]" をリストに変換
        values = eval(output)
        if isinstance(values, list) and len(values) == 3:
            results.append(values)
        else:
            print(f"Unexpected format: {output}")
    except Exception as e:
        print(f"Error parsing output: {output}")
    
    time.sleep(0.5)  # レート制限対策（必要に応じて調整）

# 結果をpandasのDataFrameに変換し、統計情報を表示
df = pd.DataFrame(results, columns=["Economic Policy", "Social Value", "Government Structure"])
#print(df.describe())

df.hist(bins=20, figsize=(12, 6))
plt.show()