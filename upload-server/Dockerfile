# Pythonのベースイメージ
FROM python:3.11.6-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースをコピー
COPY . .

# # アプリケーションを実行するコマンド
# CMD ["python", "app.py"]
# Flaskアプリケーションを 0.0.0.0 アドレスで実行するコマンド
CMD ["flask", "run", "--host=0.0.0.0", "--port=8050"]
