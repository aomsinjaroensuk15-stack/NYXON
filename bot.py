import discord
from discord.ext import commands
import requests
import os

# ดึงค่าจากระบบที่ปลอดภัย (เราจะไปตั้งใน Koyeb ทีหลัง)
TOKEN = os.getenv('DISCORD_TOKEN')
HF_TOKEN = os.getenv('HF_TOKEN')

# สมองของ NYXON (Llama 3.1 8B)
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

intents = discord.Intents.default()
intents.message_content = True # สำคัญมาก!
bot = commands.Bot(command_prefix="!", intents=intents)

def ask_nyxon(prompt):
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>คุณคือ NYXON AI ผู้ลึกลับและชาญฉลาด<|eot_id|><|start_header_id|>user<|end_header_id|>{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    # ดึงเฉพาะคำตอบออกมา
    return result[0]['generated_text'].split("assistant")[-1].strip()

@bot.event
async def on_ready():
    print(f'NYXON Online as {bot.user}')

@bot.command()
async def talk(ctx, *, message):
    async with ctx.typing():
        try:
            response = ask_nyxon(message)
            await ctx.reply(response)
        except Exception as e:
            await ctx.reply(f"ระบบขัดข้อง: {e}")

bot.run(TOKEN)
