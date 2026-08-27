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

- `!ping` - ボットのレイテンシーを確認
- `!echo [message]` - メッセージを複製
- `!help_selfbot` - ヘルプを表示

## 注意事項

⚠️ セルフボットの使用はDiscordの利用規約に違反する可能性があります。自己責任で使用してください。

## ライセンス

MIT License
