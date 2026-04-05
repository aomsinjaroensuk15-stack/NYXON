import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

# --- ระบบป้องกันการหลับ (Keep Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "NYXON Status: Online and Ready!"

def run():
    # Render จะใช้ Port 8080 เป็นค่ามาตรฐาน
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------

# ดึง Token จาก Environment Variables (ตั้งค่าใน Render)
TOKEN = os.getenv('DISCORD_TOKEN')
HF_TOKEN = os.getenv('HF_TOKEN')

# ใช้โมเดล Llama 3.1 8B ผ่าน Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def ask_nyxon(prompt):
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>คุณคือ NYXON AI ผู้ช่วยที่ชาญฉลาดและเท่<|eot_id|><|start_header_id|>user<|end_header_id|>{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result[0]['generated_text'].split("assistant")[-1].strip()

@bot.event
async def on_ready():
    print(f'Done! NYXON ตื่นแล้วในชื่อ {bot.user}')

@bot.command()
async def talk(ctx, *, message):
    async with ctx.typing():
        try:
            response = ask_nyxon(message)
            await ctx.reply(response)
        except Exception as e:
            await ctx.reply(f"เกิดข้อผิดพลาด: {e}")

# รันระบบ Keep Alive ก่อน แล้วค่อยรันบอท
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
