import os
import discord
from discord.ext import commands
from notion_client import Client
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# .envファイルから環境変数を読み込む
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Notionクライアントの初期化
notion = Client(auth=NOTION_API_KEY)

# Discordクライアントの初期化
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するために必要
bot = commands.Bot(command_prefix="!", intents=intents)

async def export_to_notion(message):
    """
    DiscordのメッセージをNotionのデータベースに書き込む
    """
    try:
        # 添付ファイルのURLをまとめる
        attachments_url = "\n".join([a.url for a in message.attachments])
        
        # 投稿日時をISO 8601形式に変換
        timestamp_iso = message.created_at.isoformat()

        # Notionにページを作成
        new_page = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Message ID": {
                    "title": [
                        {
                            "text": {
                                "content": str(message.id)
                            }
                        }
                    ]
                },
                "Author": {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"{message.author.name}#{message.author.discriminator}" if message.author.discriminator != '0' else message.author.name
                            }
                        }
                    ]
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": message.content[:2000] # Notionの文字数制限対策
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": timestamp_iso
                    }
                },
                "URL": {
                    "url": message.jump_url
                }
            }
        }

        # 添付ファイルがある場合は追加
        if attachments_url:
            new_page["properties"]["Attachments"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": attachments_url[:2000]
                        }
                    }
                ]
            }

        notion.pages.create(**new_page)
        return True
    except Exception as e:
        print(f"Error exporting message {message.id}: {e}")
        return False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    if not channel:
        print("Channel not found. Make sure the ID is correct and the bot has access.")
        await bot.close()
        return

    print(f"Fetching messages from {channel.name}...")
    
    messages = []
    # 履歴をすべて取得（量が多い場合は制限を検討）
    async for message in channel.history(limit=None, oldest_first=True):
        messages.append(message)
    
    print(f"Found {len(messages)} messages. Starting migration to Notion...")

    count = 0
    for msg in messages:
        if await export_to_notion(msg):
            count += 1
            if count % 10 == 0:
                print(f"Progress: {count}/{len(messages)}")
        # API制限（Rate Limit）を考慮して少し待機
        await asyncio.sleep(0.3)

    print(f"Migration completed! {count} messages exported.")
    await bot.close()

def main():
    if not all([DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, NOTION_API_KEY, NOTION_DATABASE_ID]):
        print("Error: Missing environment variables. Please check your .env file.")
        return
    
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
