# 🚂 Deploy บน Railway (Full-Stack)

คู่มือการ Deploy AI Medical System บน **Railway** ทั้ง Frontend และ Backend

![Railway](https://img.shields.io/badge/Railway-Deploy-blueviolet)
![Python](https://img.shields.io/badge/Python-3.11-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)

## 🎯 ทำไมต้อง Railway?

### ✅ ข้อดี
- 🚀 **Deploy ทั้ง Frontend + Backend** ในที่เดียว
- 💰 **Free Tier** ใช้งานฟรี ($5/month credit)
- 🔄 **Auto Deploy** จาก GitHub
- 🌐 **HTTPS ฟรี** อัตโนมัติ
- ⚡ **เร็ว** และใช้งานง่าย

### Railway vs Netlify
| Feature | Railway | Netlify |
|---------|---------|---------|
| Frontend | ✅ | ✅ |
| Backend (Python) | ✅ | ❌ |
| Database | ✅ | ❌ |
| Free Tier | ✅ ($5/mo) | ✅ (100GB) |

---

## 📦 เตรียมโปรเจค

### ไฟล์ที่จำเป็น (สร้างแล้ว ✅)

1. **Procfile** - บอก Railway วิธีรันแอป
   ```
   web: uvicorn backend:app --host 0.0.0.0 --port $PORT
   ```

2. **railway.json** - ตั้งค่า Railway
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn backend:app --host 0.0.0.0 --port $PORT"
     }
   }
   ```

3. **runtime.txt** - Python version
   ```
   python-3.11
   ```

4. **requirements.txt** - Python dependencies

5. **backend.py** - แก้ไขให้ serve `index.html` แล้ว ✅

---

## 🚀 วิธี Deploy (3 ขั้นตอน)

### ขั้นตอนที่ 1: Push โปรเจคขึ้น GitHub

```bash
cd AI-Medical-System

# เริ่มต้น Git
git init

# เพิ่มไฟล์ทั้งหมด
git add .

# Commit
git commit -m "Ready for Railway deployment"

# เชื่อมต่อกับ GitHub (สร้าง repo ก่อน)
git remote add origin https://github.com/yourusername/AI-Medical-System.git

# Push
git push -u origin main
```

### ขั้นตอนที่ 2: สร้างโปรเจคบน Railway

1. ไปที่ [Railway](https://railway.app/)
2. สมัครสมาชิก/Login (ใช้ GitHub Account)
3. คลิก **"New Project"**
4. เลือก **"Deploy from GitHub repo"**
5. เลือก Repository: **AI-Medical-System**
6. คลิก **"Deploy Now"**

### ขั้นตอนที่ 3: ตั้งค่า Environment Variables

1. ไปที่ **Variables** tab
2. เพิ่ม Environment Variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
PORT=8000
```

3. คลิก **"Add Variable"** → **"Redeploy"**

---

## 🎉 เสร็จแล้ว!

Railway จะ Deploy โปรเจคให้อัตโนมัติ ใช้เวลาประมาณ **2-3 นาที**

### เข้าถึงเว็บไซต์:

Railway จะสร้าง URL ให้ เช่น:
```
https://ai-medical-system-production.up.railway.app
```

- **Frontend:** `https://your-app.railway.app/`
- **API Docs:** `https://your-app.railway.app/docs`
- **Health Check:** `https://your-app.railway.app/api`

---

## 📊 โครงสร้างการทำงาน

```
┌─────────────────────────────┐
│      Railway Server         │
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
   https://your-app.railway.app
```

---

## ⚙️ การตั้งค่าเพิ่มเติม

### 1. Custom Domain (ถ้าต้องการ)

1. ไปที่ **Settings** → **Domains**
2. คลิก **"Generate Domain"** (ฟรี)
3. หรือ **"Custom Domain"** (ใช้ domain ของคุณเอง)

### 2. Environment Variables

| Variable | ค่า | จำเป็น |
|----------|-----|-------|
| `OPENAI_API_KEY` | OpenAI API Key | ✅ |
| `PORT` | 8000 | ❌ (Railway ตั้งให้อัตโนมัติ) |

### 3. ตั้งค่า Auto Deploy

Railway จะ Auto Deploy ทุกครั้งที่ Push ไปยัง GitHub โดยอัตโนมัติ ✅

ถ้าไม่ต้องการ:
1. **Settings** → **Service**
2. ปิด **"Automatic deployments"**

---

## 📁 ไฟล์ที่ต้องมี

```
AI-Medical-System/
├── Procfile              ✅ Railway start command
├── railway.json          ✅ Railway configuration
├── runtime.txt           ✅ Python version
├── requirements.txt      ✅ Python dependencies
├── backend.py            ✅ FastAPI backend (แก้ไขแล้ว)
├── index.html            ✅ Frontend
├── models/               ⚠️ YOLO models (ขนาดใหญ่)
│   ├── xray_best.pt
│   └── blood_best.pt
├── .env                  ❌ ไม่ commit (ใช้ Railway Variables)
├── .gitignore            ✅
└── README.md             ✅
```

---

## ⚠️ ข้อควรระวัง

### 1. ไฟล์ขนาดใหญ่

Railway มีขนาดจำกัด โปรเจคไม่ควรเกิน **500MB**

**ปัญหา:**
- `condition_model.pkl` (72MB) ✅ OK
- `models/*.pt` (15MB) ✅ OK
- `healthcare_dataset.csv` (8MB) ⚠️ ไม่จำเป็นต้อง commit

**แก้ไข:**
- เพิ่มใน `.gitignore`:
  ```
  healthcare_dataset.csv
  *.csv
  ```

### 2. Free Tier Limits

Railway Free Tier:
- ✅ **$5/month** credit ฟรี
- ⏰ **500 ชั่วโมง/เดือน** runtime
- 💾 **1GB** storage
- 🔄 **Unlimited** deployments

ประมาณการ:
- เว็บไซต์ของคุณใช้ประมาณ **$3-5/month** (ภายใน Free Tier!)

### 3. Cold Start

ถ้าไม่มีคนเข้าเว็บนานๆ Railway จะ "sleep" แอป:
- ครั้งแรกที่เปิดจะช้า (**10-20 วินาที**)
- ครั้งต่อไปจะเร็วปกติ

**แก้ไข:** ใช้ Cron Job ping ทุก 5 นาที (แต่จะเสีย credit เร็วขึ้น)

---

## 🔧 Troubleshooting

### ปัญหา 1: Application failed to respond

**สาเหตุ:** Port ไม่ถูกต้อง

**แก้ไข:**
- ตรวจสอบ `Procfile` ต้องมี `--port $PORT`
- Railway จะส่ง PORT environment variable มาให้

### ปัญหา 2: Module not found

**สาเหตุ:** `requirements.txt` ไม่ครบ

**แก้ไข:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### ปัญหา 3: YOLO Models ไม่โหลด

**สาเหตุ:** Path ไม่ถูกต้อง

**แก้ไข:**
```python
# backend.py
import os

# ใช้ path แบบนี้
model_path = os.path.join(os.path.dirname(__file__), "models", "xray_best.pt")
xray_model = YOLO(model_path)
```

### ปัญหา 4: 502 Bad Gateway

**สาเหตุ:** แอปใช้เวลานานในการ start (โหลด models)

**แก้ไข:**
- รอซักครู่ (1-2 นาที)
- ถ้ายังไม่ได้ ดู Logs: **Deployments** → **View logs**

### ปัญหา 5: Out of Memory

**สาเหตุ:** YOLO models ใหญ่เกินไป

**แก้ไข:**
- Upgrade Railway plan (ไม่ฟรี)
- หรือ Optimize models ให้เล็กลง

---

## 📊 Monitor & Logs

### ดู Logs
1. ไปที่ **Deployments**
2. คลิก **View logs**
3. เห็น logs แบบ real-time

### ดู Metrics
1. ไปที่ **Metrics**
2. เห็น:
   - CPU Usage
   - Memory Usage
   - Network Traffic

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
# backend.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.railway.app"],  # ระบุ domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Health Check Endpoint
```python
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

### 4. Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def home():
    logger.info("Home page accessed")
    return serve_html()
```

---

## 🎓 เรียนรู้เพิ่มเติม

### Railway Documentation
- [Official Docs](https://docs.railway.app/)
- [Python Guide](https://docs.railway.app/guides/python)
- [Environment Variables](https://docs.railway.app/guides/variables)

### Video Tutorials
- [Railway Crash Course](https://www.youtube.com/results?search_query=railway+deploy+python)
- [FastAPI on Railway](https://www.youtube.com/results?search_query=fastapi+railway)

---

## 📝 Checklist ก่อน Deploy

- [ ] สร้าง GitHub repository
- [ ] Push code ขึ้น GitHub
- [ ] ตรวจสอบ `requirements.txt` ครบถ้วน
- [ ] ลบไฟล์ที่ไม่จำเป็น (`.env`, `*.csv`)
- [ ] เตรียม `OPENAI_API_KEY`
- [ ] สร้างโปรเจคบน Railway
- [ ] ตั้งค่า Environment Variables
- [ ] Deploy และรอ 2-3 นาที
- [ ] Test ทุก feature
- [ ] เช็ค logs ว่าไม่มี error

---

## 🎉 Deploy สำเร็จ!

ตอนนี้คุณมี:
- ✅ **Frontend** ทำงานบน Railway
- ✅ **Backend API** ทำงานบน Railway
- ✅ **HTTPS** อัตโนมัติ
- ✅ **Auto Deploy** จาก GitHub
- ✅ **URL สวยๆ** แชร์ได้เลย!

**URL ตัวอย่าง:**
```
https://ai-medical-system-production.up.railway.app
```

---

<div align="center">

### 🚂 Made with Railway

**Fast • Simple • Powerful**

[Deploy Now →](https://railway.app/)

</div>