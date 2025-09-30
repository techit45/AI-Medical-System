# 🎨 Deploy บน Render (Full-Stack)

คู่มือการ Deploy AI Medical System บน **Render** ทั้ง Frontend และ Backend

![Render](https://img.shields.io/badge/Render-Deploy-46E3B7)
![Python](https://img.shields.io/badge/Python-3.11-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)

## 🎯 ทำไมต้อง Render?

### ✅ ข้อดี
- 🚀 **Deploy ทั้ง Frontend + Backend** ในที่เดียว
- 💰 **Free Tier** ใช้งานฟรีได้ (750 ชั่วโมง/เดือน)
- 🔄 **Auto Deploy** จาก GitHub
- 🌐 **HTTPS ฟรี** อัตโนมัติ
- 📊 **Easy to use** UI สวยงาม

### Render vs Railway vs Netlify

| Feature | Render | Railway | Netlify |
|---------|--------|---------|---------|
| Frontend | ✅ | ✅ | ✅ |
| Backend (Python) | ✅ | ✅ | ❌ |
| Database | ✅ | ✅ | ❌ |
| Free Tier | ✅ (750hr) | ✅ ($5/mo) | ✅ (100GB) |
| Cold Start | ~30s | ~10s | - |

---

## 📦 เตรียมโปรเจค

### ไฟล์ที่จำเป็น (สร้างแล้ว ✅)

1. **render.yaml** - Configuration file สำหรับ Render
   ```yaml
   services:
     - type: web
       name: ai-medical-system
       runtime: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn backend:app --host 0.0.0.0 --port $PORT
   ```

2. **requirements.txt** - Python dependencies

3. **backend.py** - แก้ไขให้ serve `index.html` แล้ว ✅

---

## 🚀 วิธี Deploy (4 ขั้นตอน)

### ขั้นตอนที่ 1: Push โปรเจคขึ้น GitHub

```bash
cd AI-Medical-System

# ตรวจสอบว่า push แล้วหรือยัง
git status

# ถ้ายังไม่ได้ push
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### ขั้นตอนที่ 2: สร้างบัญชี Render

1. ไปที่ [Render](https://render.com/)
2. คลิก **"Get Started for Free"**
3. เลือก **"Sign Up with GitHub"**
4. อนุญาตให้ Render เข้าถึง GitHub

### ขั้นตอนที่ 3: สร้าง Web Service

1. ที่ Dashboard คลิก **"New +"**
2. เลือก **"Web Service"**
3. เชื่อมต่อ GitHub repository: **AI-Medical-System**
4. ตั้งค่าดังนี้:

#### Basic Settings:
- **Name:** `ai-medical-system` (หรือชื่อที่ต้องการ)
- **Region:** `Singapore` (ใกล้ที่สุด)
- **Branch:** `main`
- **Runtime:** `Python 3`

#### Build Settings:
- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  uvicorn backend:app --host 0.0.0.0 --port $PORT
  ```

#### Instance Type:
- เลือก **"Free"** (750 hours/month)

### ขั้นตอนที่ 4: ตั้งค่า Environment Variables

1. ไปที่ **Environment** tab
2. คลิก **"Add Environment Variable"**
3. เพิ่ม:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. คลิก **"Save Changes"**
5. Render จะ **Auto Deploy** ให้

---

## 🎉 เสร็จแล้ว!

Render จะใช้เวลา **5-10 นาที** ในการ Deploy ครั้งแรก

### เข้าถึงเว็บไซต์:

Render จะสร้าง URL ให้ เช่น:
```
https://ai-medical-system.onrender.com
```

- **Frontend:** `https://your-app.onrender.com/`
- **API Docs:** `https://your-app.onrender.com/docs`
- **Health Check:** `https://your-app.onrender.com/api`

---

## 📊 โครงสร้างการทำงาน

```
┌─────────────────────────────┐
│      Render Server          │
│  ┌─────────────────────┐   │
│  │   FastAPI Backend   │   │
│  │    (backend.py)     │   │
│  │         ↓           │   │
│  │   Serve index.html  │   │
│  │    (Frontend)       │   │
│  └─────────────────────┘   │
│                             │
│  - Python 3.11              │
│  - YOLO Models              │
│  - LangChain + GPT-3.5      │
│  - ML Model (RandomForest)  │
└─────────────────────────────┘
          ↓
   https://your-app.onrender.com
```

---

## ⚙️ การตั้งค่าเพิ่มเติม

### 1. Custom Domain (ถ้าต้องการ)

1. ไปที่ **Settings** → **Custom Domains**
2. คลิก **"Add Custom Domain"**
3. ใส่ domain ของคุณ (เช่น `medical.yourdomain.com`)
4. ตั้งค่า DNS ตามที่ Render แนะนำ
5. รอ 24-48 ชั่วโมงให้ DNS propagate

### 2. Environment Variables

| Variable | ค่า | จำเป็น |
|----------|-----|-------|
| `OPENAI_API_KEY` | OpenAI API Key | ✅ |
| `PORT` | 10000 | ❌ (Render ตั้งให้อัตโนมัติ) |
| `PYTHON_VERSION` | 3.11.0 | ❌ |

### 3. Health Check Path

Render จะ ping `/api` ทุก 5 นาทีเพื่อตรวจสอบว่าแอปยังทำงานอยู่

### 4. Auto Deploy

Render จะ **Auto Deploy** ทุกครั้งที่ Push ไปยัง GitHub โดยอัตโนมัติ ✅

ถ้าไม่ต้องการ:
1. **Settings** → **Build & Deploy**
2. ปิด **"Auto-Deploy"**

---

## 📁 ไฟล์ที่ต้องมี

```
AI-Medical-System/
├── render.yaml           ✅ Render configuration
├── requirements.txt      ✅ Python dependencies
├── backend.py            ✅ FastAPI backend (serve HTML)
├── index.html            ✅ Frontend
├── models/               ⚠️ YOLO models (ขนาดใหญ่)
│   ├── xray_best.pt
│   └── blood_best.pt
├── .env                  ❌ ไม่ commit (ใช้ Render Variables)
├── .gitignore            ✅
└── README.md             ✅
```

---

## ⚠️ ข้อควรระวัง

### 1. ไฟล์ขนาดใหญ่

Render รองรับไฟล์ได้ไม่เกิน **500MB** ต่อ deployment

**ตรวจสอบ:**
```bash
du -sh *
```

**ปัญหา:**
- `condition_model.pkl` (72MB) ✅ OK
- `models/*.pt` (15MB) ✅ OK
- `healthcare_dataset.csv` (8MB) ⚠️ ไม่จำเป็นต้อง commit

**แก้ไข:** เพิ่มใน `.gitignore`

### 2. Free Tier Limits

Render Free Tier:
- ✅ **750 ชั่วโมง/เดือน** (ประมาณ 31 วัน)
- 💾 **512MB RAM**
- 💿 **1GB Storage**
- ⏰ **15 นาที auto-sleep** (ถ้าไม่มีคนเข้า)

**Cold Start:**
- Free tier จะ "sleep" หลังไม่มีคนเข้า 15 นาที
- ครั้งแรกที่เปิดจะช้า (**30-60 วินาที**)
- ครั้งต่อไปจะเร็วปกติ

### 3. RAM Limit

**ปัญหา:** YOLO models อาจใช้ RAM เกิน 512MB

**แก้ไข:**
1. Upgrade เป็น Paid plan ($7/month = 2GB RAM)
2. หรือ Optimize models:
   ```python
   # Load model เฉพาะตอนใช้งาน
   from functools import lru_cache

   @lru_cache(maxsize=1)
   def get_xray_model():
       return YOLO("models/xray_best.pt")
   ```

### 4. Build Time

Free tier มี **build timeout 15 นาที**

ถ้า build เกิน ให้:
- ลด dependencies ใน `requirements.txt`
- หรือ Upgrade เป็น Paid plan

---

## 🔧 Troubleshooting

### ปัญหา 1: Application failed to start

**สาเหตุ:** Port ไม่ถูกต้อง

**แก้ไข:**
```bash
# startCommand ต้องมี --port $PORT
uvicorn backend:app --host 0.0.0.0 --port $PORT
```

### ปัญหา 2: Build failed

**สาเหตุ:** `requirements.txt` ไม่ครบหรือ Python version ไม่ตรง

**แก้ไข:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### ปัญหา 3: Module not found

**สาเหตุ:** Package ไม่อยู่ใน `requirements.txt`

**แก้ไข:**
```bash
pip install <package-name>
pip freeze > requirements.txt
```

### ปัญหา 4: Out of memory

**สาเหตุ:** YOLO models ใหญ่เกินไป (512MB RAM)

**แก้ไข:**
- Upgrade เป็น Paid plan ($7/month)
- หรือ Deploy Backend แยก + Static Site

### ปัญหา 5: Slow cold start

**สาเหตุ:** Free tier sleep หลัง 15 นาที

**แก้ไข:**
- ใช้ Cron Job ping ทุก 10 นาที (แต่จะเสีย free hours)
- หรือ Upgrade เป็น Paid plan (ไม่มี sleep)

---

## 📊 Monitor & Logs

### ดู Logs แบบ Real-time

1. ไปที่ Dashboard
2. คลิกที่ Service name
3. เลือก **"Logs"** tab
4. เห็น logs แบบ real-time

### ดู Metrics

1. เลือก **"Metrics"** tab
2. เห็น:
   - CPU Usage
   - Memory Usage
   - Response Time
   - Request Count

---

## 💡 Tips & Best Practices

### 1. ใช้ Environment Variables

```python
# ❌ อย่าทำ
api_key = "sk-proj-xxxx"

# ✅ ทำแบบนี้
import os
api_key = os.getenv("OPENAI_API_KEY")
```

### 2. Enable CORS อย่างปลอดภัย

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Health Check Endpoint

```python
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

### 4. Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")
```

### 5. Optimize Build Time

```python
# ใช้ --no-cache-dir เพื่อลด disk usage
pip install --no-cache-dir -r requirements.txt
```

---

## 🔄 Update & Redeploy

### Manual Deploy

1. ไปที่ **Manual Deploy**
2. เลือก branch
3. คลิก **"Deploy latest commit"**

### Auto Deploy (แนะนำ)

Push code ขึ้น GitHub แล้ว Render จะ deploy อัตโนมัติ:

```bash
git add .
git commit -m "Update features"
git push origin main
```

---

## 📈 Monitoring

### 1. Uptime Monitoring

ใช้ [UptimeRobot](https://uptimerobot.com/) ping ทุก 5 นาที:
- Free
- แจ้งเตือนเมื่อเว็บ down
- ป้องกัน cold start

### 2. Error Tracking

ใช้ [Sentry](https://sentry.io/):
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## 💰 ราคา Render

### Free Tier (แนะนำสำหรับเริ่มต้น)
- ✅ **750 ชั่วโมง/เดือน** ฟรี
- 💾 **512MB RAM**
- ⏰ Sleep หลัง 15 นาที ไม่มีคนเข้า

### Starter Plan - $7/month
- ✅ **ไม่มี sleep**
- 💾 **2GB RAM**
- ⚡ **Fast cold start**
- 📊 **Priority support**

---

## 📝 Checklist ก่อน Deploy

- [ ] Push code ขึ้น GitHub
- [ ] สร้าง Render account
- [ ] เตรียม `OPENAI_API_KEY`
- [ ] สร้าง Web Service บน Render
- [ ] ตั้งค่า Environment Variables
- [ ] Deploy และรอ 5-10 นาที
- [ ] Test ทุก feature
- [ ] เช็ค logs ว่าไม่มี error
- [ ] ตั้งค่า Custom Domain (ถ้าต้องการ)

---

## 🎉 Deploy สำเร็จ!

ตอนนี้คุณมี:
- ✅ **Frontend** ทำงานบน Render
- ✅ **Backend API** ทำงานบน Render
- ✅ **HTTPS** อัตโนมัติ
- ✅ **Auto Deploy** จาก GitHub
- ✅ **URL สวยๆ** แชร์ได้เลย!

**URL ตัวอย่าง:**
```
https://ai-medical-system.onrender.com
```

---

## 🎓 เรียนรู้เพิ่มเติม

- [Render Documentation](https://render.com/docs)
- [Deploy FastAPI](https://render.com/docs/deploy-fastapi)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Custom Domains](https://render.com/docs/custom-domains)

---

<div align="center">

### 🎨 Made with Render

**Fast • Simple • Reliable**

[Deploy Now →](https://render.com/)

</div>