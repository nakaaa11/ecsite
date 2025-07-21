# Green Harvest - 地産地消のヘルシー食材ECサイト

Djangoで構築された地産地消・ヘルシー食材のECサイトです。

## 機能

- 商品一覧・詳細表示
- カート機能（数量選択・非同期追加）
- ユーザー認証（通常ログイン・Googleソーシャルログイン）
- Stripe決済連携
- 注文履歴管理
- レスポンシブデザイン（Bootstrap 5）

## 技術スタック

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite（開発）/ PostgreSQL（本番推奨）
- **決済**: Stripe
- **認証**: django-allauth（Googleソーシャルログイン）
- **画像**: Pillow

## セットアップ

### 1. 環境構築

```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化（Windows）
.\venv\Scripts\Activate.ps1

# 依存パッケージインストール
pip install -r requirements.txt
```

### 2. データベース設定

```bash
# マイグレーション実行
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser

# ダミーデータ投入
python manage.py seed_products
```

### 3. 環境変数設定

`.env`ファイルを作成し、以下を設定：

```
SECRET_KEY=your-secret-key
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### 4. サーバー起動

```bash
python manage.py runserver
```

## 主要機能

### 商品管理
- 商品のCRUD操作
- 画像アップロード
- 在庫管理

### カート機能
- 数量選択
- 非同期追加（画面遷移なし）
- カート内商品削除

### 決済システム
- Stripe決済連携
- 金額表示（3桁区切りカンマ）
- 決済完了メール送信

### ユーザー管理
- 通常ログイン
- Googleソーシャルログイン
- 注文履歴表示

## 本番運用に向けて

### 必須対応項目
1. **セキュリティ設定**
   - DEBUG = False
   - 本番用SECRET_KEY
   - ALLOWED_HOSTS設定

2. **データベース移行**
   - SQLite → PostgreSQL

3. **静的ファイル設定**
   - STATIC_ROOT設定
   - 静的ファイル収集

4. **決済システム**
   - Stripe本番キー設定
   - Webhook設定

### 推奨追加機能
- 配送システム連携
- 在庫管理機能
- レビュー・評価機能
- クーポン・ポイントシステム
- メール配信機能

## 開発者

- フルスタック開発
- Django/Python
- フロントエンド（Bootstrap/JavaScript）

## ライセンス

MIT License 