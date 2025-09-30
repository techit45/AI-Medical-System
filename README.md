# 🏥 AI Medical System

ระบบปัญญาประดิษฐ์ทางการแพทย์ครบวงจร สำหรับวิเคราะห์ภาพทางการแพทย์ ทำนายโรค และให้คำปรึกษาผ่าน AI Chatbot

![AI Medical System](https://img.shields.io/badge/AI-Medical%20System-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)
![YOLO](https://img.shields.io/badge/YOLO-v8-orange)

## 📋 ภาพรวมโปรเจค

ระบบ AI Medical Assistant ที่พัฒนาด้วย Deep Learning, Computer Vision และ Natural Language Processing เพื่อช่วยเหลือในการวิเคราะห์ข้อมูลทางการแพทย์ ประกอบด้วย:

- 🩻 **วิเคราะห์ภาพ X-Ray** - ใช้ YOLO Model ความแม่นยำ 95%+
- 🩸 **ตรวจเซลล์เลือด** - Object Detection นับและแยกประเภทเซลล์อัตโนมัติ
- 🧠 **ทำนายโรค** - RandomForest ML Model ทำนาย 6 ประเภทโรคด้วยความแม่นยำ 98%
- 🤖 **AI Chatbot** - LangChain + GPT-3.5 ให้คำปรึกษาทางการแพทย์

## ✨ ฟีเจอร์หลัก

### 1. 🖼️ วิเคราะห์ภาพทางการแพทย์

- อัพโหลดและวิเคราะห์ภาพ X-Ray
- ตรวจจับและนับเซลล์เลือด
- แสดงผลความมั่นใจและรายละเอียด

### 2. 📝 ระบบซักประวัติอาการ

- ซักถามอาการผู้ป่วย 7 ข้อ
- ทำนายโรคที่เป็นไปได้ด้วย ML
- แสดง Confidence Score และ Probabilities

### 3. 💬 Medical Chatbot

- สนทนาด้วย LangChain + OpenAI GPT-3.5
- จดจำบทสนทนาด้วย ConversationBufferMemory
- ค้นหาข้อมูลผู้ป่วยจากฐานข้อมูล

### 4. 📊 สถิติและข้อมูลผู้ป่วย

- แสดงสถิติผู้ป่วย 10,000+ รายการ
- ค้นหาข้อมูลตามชื่อ อาการ หรือกรุ๊ปเลือด
- กราฟและการวิเคราะห์ข้อมูล

## 🛠️ เทคโนโลยีที่ใช้

### Backend

- **FastAPI** - REST API Framework
- **Python 3.9+** - Programming Language
- **Uvicorn** - ASGI Server

### AI/ML

- **YOLO (Ultralytics)** - Object Detection สำหรับ X-Ray และเซลล์เลือด
- **Scikit-learn** - RandomForest Classifier สำหรับทำนายโรค
- **LangChain** - Framework สำหรับ AI Chatbot
- **OpenAI GPT-3.5** - Large Language Model

### Data Processing

- **Pandas** - Data Analysis
- **NumPy** - Numerical Computing
- **PyTorch** - Deep Learning Framework
- **OpenCV** - Computer Vision

### Frontend

- **HTML/CSS/JavaScript** - UI/UX
- **Font Awesome** - Icons

## 📦 การติดตั้ง

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Medical-System.git
cd AI-Medical-System
```

### 2. สร้าง Virtual Environment

```bash
python -m venv env
source env/bin/activate  # MacOS/Linux
# หรือ
env\Scripts\activate  # Windows
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า Environment Variables

สร้างไฟล์ `.env` และใส่ API Key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. เตรียมข้อมูล

- วาง `healthcare_dataset.csv` ในโฟลเดอร์หลัก
- วาง YOLO models (`xray_best.pt`, `blood_best.pt`) ในโฟลเดอร์ `models/`

## 🚀 การใช้งาน

### รันเซิร์ฟเวอร์

```bash
python backend.py
```

หรือ

```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

### เข้าถึงเว็บแอปพลิเคชัน

เปิดเบราว์เซอร์และไปที่:

```
http://localhost:8000
```

หรือเปิดไฟล์ `index.html` โดยตรง

### API Documentation

FastAPI มี API Documentation อัตโนมัติ:

```
http://localhost:8000/docs
```

## 📁 โครงสร้างโปรเจค

```
AI-Medical-System/
├── backend.py              # FastAPI Backend Server
├── index.html              # Frontend (Deepseek.html)
├── requirements.txt        # Python Dependencies
├── models/                 # YOLO Models
│   ├── xray_best.pt
│   └── blood_best.pt
├── healthcare_dataset.csv  # Patient Data (ไม่ต้อง commit)
├── condition_model.pkl     # ML Model (ไม่ต้อง commit)
├── .env                    # Environment Variables (ไม่ต้อง commit)
└── README.md              # Documentation
```

## 📊 API Endpoints

| Method | Endpoint           | Description              |
| ------ | ------------------ | ------------------------ |
| GET    | `/`                | Health Check             |
| POST   | `/analyze`         | วิเคราะห์ภาพ X-Ray/เลือด |
| POST   | `/symptom/start`   | เริ่มซักประวัติอาการ     |
| POST   | `/symptom/answer`  | ตอบคำถามอาการ            |
| POST   | `/chat`            | แชทกับ AI Chatbot        |
| POST   | `/patient/search`  | ค้นหาข้อมูลผู้ป่วย       |
| GET    | `/patient/stats`   | ดูสถิติผู้ป่วย           |
| GET    | `/chat/clear/{id}` | ลบประวัติแชท             |

## 🎯 ผลลัพธ์

- ✅ **95%+** ความแม่นยำในการวิเคราะห์ X-Ray
- ✅ **98%** ความแม่นยำในการทำนายโรคด้วย ML Model
- ✅ **10,000+** รายการข้อมูลผู้ป่วยในระบบ
- ✅ **4** ฟีเจอร์หลักที่พร้อมใช้งาน

## 🔒 ข้อควรระวัง

### Security

- **ไม่ควร commit** ไฟล์ `.env` ที่มี API Keys
- **ไม่ควร commit** ไฟล์ข้อมูลขนาดใหญ่ (`*.pkl`, `*.csv`)
- ใช้ Environment Variables สำหรับข้อมูลสำคัญ
- เพิ่ม Authentication/Authorization ก่อนใช้งานจริง

### Medical Disclaimer

⚠️ **ระบบนี้เป็นเพียง Demo/Prototype เท่านั้น**

- ไม่ควรนำไปใช้ในการวินิจฉัยโรคจริง
- ผลลัพธ์เป็นเพียงการประเมินเบื้องต้น
- ควรปรึกษาแพทย์เสมอสำหรับการวินิจฉัยที่แม่นยำ

## 👨‍💻 ผู้พัฒนา

พัฒนาโดย: **นักศึกษา Computer Science, KMUTT**

ปี: 2024-2025

## 📝 License

This project is for educational purposes only.

## 🙏 Acknowledgments

- YOLO by Ultralytics
- LangChain Framework
- OpenAI GPT Models
- FastAPI Framework
- Healthcare Dataset (Source)

---
