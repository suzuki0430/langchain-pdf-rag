# Pythonのイメージをベースにする
FROM python:3.11.6-slim

# 必要なツールのインストール
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースをコピー
COPY . .

# Flaskアプリケーションを実行するコマンドだがdocker-compose.ymlのコマンドが優先される
CMD ["flask", "--app", "app.web", "run", "--host=0.0.0.0"]
