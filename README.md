# Discord Self-Bot

自分のDiscordアカウントで動作するセルフボットです。

## セットアップ方法

### 1. リポジトリをクローン
```bash
git clone https://github.com/0pointshaka/discord-selfbot.git
cd discord-selfbot
```

### 2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

### 3. Discordトークンを取得
1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 新しいアプリケーションを作成
3. "Bot" セクションから "Add Bot" をクリック
4. トークンをコピー

### 4. 環境変数を設定
`.env` ファイルを編集して、取得したトークンを入力：
```
DISCORD_TOKEN=your_token_here
```

### 5. ボットを実行
```bash
python main.py
```

## 利用可能なコマンド

### 基本コマンド

| コマンド | 説明 |
|---------|------|
| `!ping` | ボットのレイテンシーを確認 |
| `!echo [message]` | メッセージを複製 |
| `!help_selfbot` | 利用可能なコマンドを表示 |

### サーバー管理コマンド

#### `!delete_all_channels`
サーバー内のすべてのチャンネルを削除します。

**機能:**
- ✅ 確認機能（リアクション選択式）
- ✅ 30秒のタイムアウト機能
- ✅ 削除進行状況をリアルタイム表示
- ✅ 削除完了時に結果サマリーを表示

**使い方:**
```
!delete_all_channels
```

⚠️ **警告:** このコマンドで削除されたチャンネルは復元できません。実行前に必ず確認が表示されます。

#### `!export_server_logs [webhook_url]`
サーバーの詳細ログをWebhook経由で送信します。

**エクスポート対象:**
- 📊 サーバー基本情報（名前、ID、メンバー数、チャンネル数、ロール数）
- 📁 チャンネル一覧（名前、タイプ、ID、作成日時）
- 👥 メンバー情報（上限50名、ユーザー名、ID、参加日時、ロール）
- 🎭 ロール情報（上限20個、名前、ID、カラー、メンバー数）

**使い方:**
```
!export_server_logs https://discord.com/api/webhooks/YOUR_WEBHOOK_URL
```

**Webhook URLの取得方法:**
1. Discordサーバーでウェブフック作成権限を確認
2. サーバー設定 → ウェブフック → 新しいウェブフック作成
3. URLをコピーしてコマンドに渡す

## 注意事項

⚠️ **セルフボットの使用について**
- セルフボットの使用はDiscordの利用規約に違反する可能性があります
- 自己責任で使用してください
- サーバーの所有者から許可を得てください

## ライセンス

MIT License
