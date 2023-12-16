# 概要

PDF を Retriever とした AI チャットボット。

# ローカル環境構築

## 事前準備

`.env`で環境変数を設定する。

## 構築手順

1. コンテナ起動

```bash
docker-compose up --build
```

2. DB 初期化

```bash
docker exec -it [コンテナ名] flask --app app.web init-db
```
