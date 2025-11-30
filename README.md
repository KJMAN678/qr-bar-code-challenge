# QRコード / バーコード ジェネレーター

## 概要

テキストを入力して、様々な規格のQRコードやバーコードを生成・表示・管理できるWebアプリケーションです。

## 対応コード仕様

### QRコード
- **QRコード (モデル2)**
  - **特徴**: 現在最も広く普及しているQRコードの規格で、数字、英数字、バイナリデータ、漢字など多様なデータを格納できます。
  - **データ容量**: 最大で数字7,089桁、英数字4,296文字を格納可能です。
  - **用途**: URLリンク、決済、電子チケットなど非常に幅広い用途で利用されています。
- **マイクロQR**
  - **特徴**: 通常のQRコードを小型化した規格で、印刷スペースが限られている場合に適しています。
  - **データ容量**: 最大で数字35桁、英数字21文字とデータ量は少なめです。
  - **用途**: 電子部品の管理ラベルなど、小さなスペースへの印字が必要な場面で利用されます。

### バーコード
- **Code39**
  - **特徴**: 数字(0-9)、アルファベット大文字(A-Z)、一部の記号(-, ., $, /, +, %, スペース)を表現できます。
  - **用途**: 工業製品の部品管理や資産管理ラベルなど、業務用途で広く利用されています。
- **Code128**
  - **特徴**: ASCIIコードで表現できる128文字すべてを扱える高密度なバーコードです。
  - **用途**: 物流、在庫管理、医療材料の識別など、多様な業界で利用されています。
- **EAN-13 / EAN-8**
  - **特徴**: 商品の識別に使われる国際的な標準コードです。13桁または8桁の数字で構成されます。(日本のJANコードもEANの一種です)
  - **用途**: 小売店で販売される商品の商品コードとして、世界中で利用されています。
- **UPC-A / UPC-E**
  - **特徴**: 主にアメリカやカナダで使われている商品コードです。12桁または8桁(短縮版)の数字で構成されます。
  - **用途**: EANと同様に、小売商品の識別に使用されます。
- **ITF (Interleaved 2 of 5)**
  - **特徴**: 数字のみを表現できる高密度なバーコードで、必ず偶数桁のデータで構成されます。
  - **用途**: 物流の段ボール箱など、商品の集合包装の識別に広く利用されています。

---
### Devin

- [Devin's Machine](https://app.devin.ai/workspace) でリポジトリ追加

#### 1.Git Pull
- そのまま

#### 2.Configure Secrets
```sh
# 環境変数用のファイル作成
$ touch .envrc
$ cp .envrc.example .envrc
$ direnv allow
```

- ローカル用
```sh
$ brew install direnv
```
#### 4.Maintain Dependencies
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml up -d
# Devin用
$ docker compose -f docker-compose.ubuntu.yaml up -d

# コンテナ作り直し
$ ./remake-container.sh mac
$ ./remake-container.sh ubuntu
```

#### 5.SetUp Lint
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run ruff check .
$ docker compose -f docker-compose.mac.yaml run --rm frontend npx next lint

# Devin用
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run ruff check .
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npx next lint
```

#### 6.SetUp Tests
- no tests ran in 0.00s だと Devin の Verify が通らないっぽい
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run pytest
$ docker compose -f docker-compose.mac.yaml run --rm frontend npm run test

# Devin用
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run pytest
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npm run test

# Playwright
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml run --rm frontend npx playwright test --project firefox

# Devin用
# Playwright
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npx playwright test --project firefox
```

### 7.Setup Local App

```sh
$ http://localhost:3000/ がフロントエンドのURL
$ http://localhost:8000/ がバックエンドのURL
```

#### 8.Additional Notes
- 必ず日本語で回答してください
を入力

### OPENAI-API で PR-Review
- [Qodo Merge](https://qodo-merge-docs.qodo.ai/installation/github/)
  - GPT-4.1利用
  - 日本語の回答をするようプロンプト設定
- GitHub の Repository >> Settings >> Secretes and variables >> Actions の Repository secrets の New repository secret を登録
  - OPENAI_KEY という名称で OPENAI API keys の SECRET KEY を登録
    - [OPENAI API keys](https://platform.openai.com/settings/organization/api-keys) 
```sh
--- .github/
           |- workflows/
                        |-- pr_agent.yml
```
### Django
- app 追加
```sh
# ローカルM1Mac用
$ mkdir -p backend/app/api
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run django-admin startapp api app/api
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run python app/manage.py makemigrations
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run python app/manage.py migrate

# Devin用
$ mkdir -p backend/app/api
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run django-admin startapp api app/api
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run python app/manage.py makemigrations
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run python app/manage.py migrate
```

### package-json, package-json-lock のアプデ
```sh
$ cd frontend
$ npx npm-check-updates -u
$ npx npm-check-updates -u --target minor
$ npx npm-check-updates -u --target patch
$ npm install
$ cd ..
```
