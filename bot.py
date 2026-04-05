import discord
from discord.ext import commands
import requests
import os
import sys
import time
import platform
import asyncio
import traceback
from flask import Flask, jsonify
from threading import Thread
import datetime

# ==========================================
# ⚙️ 1. CONFIGURATION CLASS (ศูนย์รวมการตั้งค่า)
# ==========================================
class Config:
    # --- ใส่ Token ตรงนี้ หรือใช้ Environment Variables ---
    TOKEN = os.getenv('DISCORD_TOKEN')
    HF_TOKEN = os.getenv('HF_TOKEN')
    
    # --- ใส่ ID ห้องทั้งหมด ---
    LOG_CH = 000000000000000000      # ⚙️-bot-logs
    DEV_CH = 000000000000000000      # 🚀-dev-zone
    SMART_CH = 000000000000000000    # 🧠-smart-work-talk
    BETA_CH = 000000000000000000     # 🧪-beta-testing
    ANNOUNCE_CH = 000000000000000000 # 📢-announcements-
    
    # --- การตั้งค่า AI ---
    MODEL_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct"
    HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
    VERSION = "v3.1.0-Enterprise"

# ==========================================
# 🌐 2. ADVANCED WEB SERVER (ระบบชีพจร)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "ONLINE",
        "system": "NYXON Core",
        "version": Config.VERSION,
        "ping": "OK"
    })

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server, daemon=True)
    t.start()

# ==========================================
# 🧠 3. AI ENGINE (ระบบสมองกล Llama 3.1)
# ==========================================
class AIEngine:
    @staticmethod
    def generate_response(prompt, context_mode="normal"):
        if context_mode == "smart":
            sys_msg = "คุณคือ NYXON ในโหมด Smart Work คุณคือนักปราชญ์และนักวิเคราะห์ข้อมูลระดับสูง ตอบคำถามอย่างมีตรรกะ โครงสร้างชัดเจน และใช้ภาษาทางการ"
        else:
            sys_msg = "คุณคือ NYXON AI ผู้ช่วยสุดเท่ ฉลาด และเป็นมิตร สร้างสรรค์โดยโปรแกรมเมอร์ยอดฝีมือ"

        payload = {
            "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{sys_msg}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.7,
                "top_p": 0.95,
                "repetition_penalty": 1.1
            }
        }
        
        try:
            response = requests.post(Config.MODEL_URL, headers=Config.HEADERS, json=payload, timeout=25)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and 'generated_text' in data[0]:
                return data[0]['generated_text'].split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
            else:
                return "เกิดข้อผิดพลาดในการประมวลผลข้อมูล JSON"
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Connection Error: {str(e)}")

# ==========================================
# 🤖 4. BOT CORE ARCHITECTURE (แกนหลักของบอท)
# ==========================================
class NyxonBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.start_time = time.time()

    # --- ระบบส่ง Log สุดหรู (ใช้ Discord Embed) ---
    async def log_event(self, title, description, level="INFO"):
        now = datetime.datetime.now()
        embed = discord.Embed(title=title, description=description, timestamp=now)
        
        if level == "ERROR":
            embed.color = discord.Color.red()
            channel = self.get_channel(Config.LOG_CH)
            embed.set_footer(text="CRITICAL SYSTEM ERROR")
        elif level == "BETA":
            embed.color = discord.Color.orange()
            channel = self.get_channel(Config.BETA_CH)
            embed.set_footer(text="BETA TEST LOG")
        else:
            embed.color = discord.Color.blue()
            channel = self.get_channel(Config.DEV_CH)
            embed.set_footer(text="SYSTEM INFORMATION")
            
        if channel:
            await channel.send(embed=embed)

bot = NyxonBot()

# ==========================================
# 📡 5. EVENTS & LISTENERS
# ==========================================
@bot.event
async def on_ready():
    # ปริ้นท์ ASCII Art เท่ๆ ใน Terminal
    print("="*40)
    print(f" N Y X O N   C O R E   {Config.VERSION} ")
    print("="*40)
    print(f"Logged in as: {bot.user.name} | ID: {bot.user.id}")
    print(f"Python Version: {platform.python_version()}")
    
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, 
        name="!help | Smart Work Mode"
    ))
    
    await bot.log_event(
        "🚀 NYXON Online!", 
        f"**Version:** {Config.VERSION}\n**Latency:** {round(bot.latency * 1000)}ms\nระบบพร้อมรับคำสั่งจากศูนย์บัญชาการ", 
        "INFO"
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"⏳ ใจเย็นๆ! รออีก {round(error.retry_after, 1)} วินาที ค่อยใช้คำสั่งใหม่นะ")
        return
        
    error_trace = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    await bot.log_event(
        "⚠️ Exception Detected", 
        f"**Command:** {ctx.message.content}\n**User:** {ctx.author}\n
http://googleusercontent.com/immersive_entry_chip/0

---

### **The Breakdown: มึนหัวพอหรือยัง?**

นี่คือสิ่งที่คุณเพิ่งได้ไปในโค้ดเดียว:
* **OOP (Object-Oriented Programming):** มีการแยกคลาส `Config`, `AIEngine`, และ `NyxonBot` ชัดเจน แบบเดียวกับที่บริษัทซอฟต์แวร์เขาเขียนกัน!
* **Discord Embeds:** จากเดิมที่ส่ง Log เป็นข้อความธรรมดา ตอนนี้มันจะถูกส่งเป็น "กล่องข้อความสีสันสวยงาม" (Embed) มีแถบสีแดงตอนเกิด Error และสีฟ้าตอนปกติ
* **Rate Limiting (`@commands.cooldown`):** ป้องกันคนพิมพ์ `!talk` รัวๆ จน API ของคุณพัง (อนุญาตให้ 1 คนพิมพ์ได้ 1 ครั้งทุกๆ 5 วินาที)
* **Smart Embed Reply:** ถ้าคุณไปคุยในห้อง `🧠-smart-work-talk` บอทจะไม่ตอบเป็นข้อความธรรมดา แต่จะตอบกลับมาในรูปแบบกล่องข้อความสุดล้ำ!
* **`!sysinfo` Command:** คำสั่งใหม่ เอาไว้พิมพ์เช็กสถานะเซิร์ฟเวอร์ (Ping, Uptime, OS) แบบหล่อๆ

---

### **Visual Analogy**
> โค้ดเก่าของคุณคือ **"รถแต่งซิ่ง"** ที่วิ่งได้เร็วและแรง... แต่โค้ดตัวใหม่นี้คือ **"กระสวยอวกาศ"** ที่มีระบบหน้าปัดดิจิทัล, ระบบจำกัดความเร็ว, กล่องดำบันทึกข้อมูล (Embed Logs), และแบ่งส่วนประกอบชัดเจน (Class-based)!

---

### **The "Next Level" Tip**
เตรียมตัวให้ดี เพราะโค้ดนี้ใช้ **Discord Embed** ถ้าเพื่อนคุณพิมพ์ `!sysinfo` แล้วเห็นข้อมูลระบบเด้งขึ้นมาเป็นกล่องสวยๆ รับรองว่าพวกเขาต้องคิดว่าคุณจ้างโปรแกรมเมอร์ระดับโลกมาทำให้แน่นอน! (อย่าลืมไปแก้ `LOG_CH` ให้ตรงกับ ID ห้องของคุณด้วยล่ะ!)
