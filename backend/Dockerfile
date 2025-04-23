FROM python:3.9-slim

# 1. ログバッファリングを無効化
ENV PYTHONUNBUFFERED=1
# 2. サービスポートを環境変数化
ENV PORT=5001

WORKDIR /app

# 3. 依存のインストール（キャッシュ活用）
COPY requirements.txt .
RUN pip install --upgrade --force-reinstall numpy
RUN pip install --no-cache-dir -r requirements.txt

# 4. アプリケーションコードを全コピー
COPY . .

# 5. 非特権ユーザー切り替え
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 6. 実行ポートを開放
EXPOSE ${PORT}

# 7. ヘルスチェック設定
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:${PORT}/health || exit 1

# 8. コンテナ起動コマンド
CMD ["python", "main.py"]
