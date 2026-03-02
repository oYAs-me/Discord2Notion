# Discord to Notion 移行ガイド

このガイドでは、Discordのメッセージ履歴をNotionのデータベースに移植するための設定手順を説明します。

## 1. Discordの設定

### 1.1. Discordボットの作成
1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセスします。
2. **New Application** をクリックし、名前（例: `Discord2Notion`）を入力して作成します。
3. 左メニューの **Bot** を選択します。
4. **Reset Token** をクリックしてトークンを発行し、コピーしておきます（これが `DISCORD_BOT_TOKEN` になります）。
5. **重要:** 同じページ内の **Privileged Gateway Intents** セクションにある **MESSAGE CONTENT INTENT** を **ON** に設定してください。これがないとメッセージの内容を読み取れません。

### 1.2. ボットのサーバー招待
1. 左メニューの **OAuth2** -> **URL Generator** を選択します。
2. **Scopes** で `bot` にチェックを入れます。
3. **Bot Permissions** で以下にチェックを入れます：
   - `Read Messages/View Channels`
   - `Read Message History`
4. 下部に表示されたURLをコピーしてブラウザで開き、対象のDiscordサーバーにボットを招待します。

### 1.3. チャンネルIDの取得
1. Discordアプリの **ユーザー設定** -> **詳細設定** -> **開発者モード** を **ON** にします。
2. 移植したいチャンネルを右クリックし、**「チャンネルIDをコピー」** を選択します（これが `DISCORD_CHANNEL_ID` になります）。

---

## 2. Notionの設定

### 2.1. インテグレーションの作成
1. [Notion My Integrations](https://www.notion.so/my-integrations) にアクセスします。
2. **+ 新しいインテグレーション** を作成します。
3. **内部インテグレーションシークレット** をコピーしておきます（これが `NOTION_API_KEY` になります）。

### 2.2. データベースの作成
1. Notionで新しいデータベースを作成します。
2. **プロパティ名** と **型** を以下の通りに設定してください（名前が一致している必要があります）：
   - `Message ID`: **タイトル** (Title)
   - `Author`: **テキスト** (Text)
   - `Content`: **テキスト** (Text)
   - `Date`: **日付** (Date)
   - `URL`: **URL**
   - `Attachments`: **テキスト** (Text) ※任意

### 2.3. データベースへのアクセス許可
1. 作成したデータベースページの右上にある「**...**」ボタンをクリックします。
2. **接続先を追加** (Add connections) を選択し、作成したインテグレーション名を探して追加します。

### 2.4. データベースIDの取得
1. データベースのURLを確認します：
   `https://www.notion.so/myworkspace/`**`DATABASE_ID`**`?v=...`
2. ワークスペース名と `?` の間にある32文字の英数字が `NOTION_DATABASE_ID` です。

---

## 3. 環境設定

1. プロジェクトルートにある `.env.template` をコピーして `.env` ファイルを作成します。
2. 取得した各値を入力します：

```env
DISCORD_BOT_TOKEN=あなたのDiscordボットトークン
DISCORD_CHANNEL_ID=移行したいチャンネルのID
NOTION_API_KEY=あなたのNotion APIキー
NOTION_DATABASE_ID=あなたのNotionデータベースID
```

---

## 4. 実行方法

設定が完了したら、以下のコマンドでスクリプトを実行してください。

```bash
uv run main.py
```
