# 📝 วิธีสร้าง GitHub Repository และ Push Code

## ขั้นตอนที่ 1: สร้าง Repository บน GitHub

### 1.1 เข้าสู่ GitHub
1. ไปที่ [GitHub](https://github.com/)
2. Login เข้าสู่บัญชีของคุณ

### 1.2 สร้าง Repository ใหม่
1. คลิกปุ่ม **"+"** ที่มุมขวาบน
2. เลือก **"New repository"**
3. ตั้งค่าดังนี้:
   - **Repository name:** `AI-Medical-System`
   - **Description:** `ระบบ AI Medical Assistant ด้วย FastAPI + YOLO + LangChain`
   - **Public** หรือ **Private** (แล้วแต่คุณ)
   - ❌ **ไม่ต้องเลือก** "Add a README file"
   - ❌ **ไม่ต้องเลือก** ".gitignore"
   - ❌ **ไม่ต้องเลือก** "Choose a license"
4. คลิก **"Create repository"**

---

## ขั้นตอนที่ 2: เชื่อมต่อกับ GitHub

### 2.1 คัดลอก URL ของ Repository
หลังสร้าง Repository เสร็จ GitHub จะแสดง URL เช่น:
```
https://github.com/YOUR_USERNAME/AI-Medical-System.git
```

**สำคัญ:** แทนที่ `YOUR_USERNAME` ด้วยชื่อ GitHub ของคุณ!

### 2.2 ตั้งค่า Git Remote

```bash
cd /Users/techit/Desktop/Login-Learning/Cource/AIForMed/AiForMed/Test/AI-Medical-System

# ลบ remote เก่า (ถ้ามี)
git remote remove origin

# เพิ่ม remote ใหม่ (แทนที่ YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AI-Medical-System.git

# ตรวจสอบว่าตั้งค่าถูกต้อง
git remote -v
```

---

## ขั้นตอนที่ 3: Push Code ขึ้น GitHub

```bash
# ตรวจสอบสถานะ
git status

# เพิ่มไฟล์ทั้งหมด (ถ้ายังไม่ได้ add)
git add .

# Commit (ถ้ายังไม่ได้ commit)
git commit -m "Initial commit: AI Medical System for Railway deployment"

# เปลี่ยน branch เป็น main (ถ้ายังเป็น master)
git branch -M main

# Push ขึ้น GitHub
git push -u origin main
```

---

## ❗ ถ้าเจอ Error: Authentication Required

### วิธีแก้: ใช้ Personal Access Token (PAT)

#### 1. สร้าง Personal Access Token
1. ไปที่ GitHub → **Settings**
2. เลือก **Developer settings** (ด้านซ้ายล่าง)
3. เลือก **Personal access tokens** → **Tokens (classic)**
4. คลิก **"Generate new token"** → **"Generate new token (classic)"**
5. ตั้งค่า:
   - **Note:** `AI Medical System`
   - **Expiration:** 90 days (หรือตามต้องการ)
   - **Select scopes:** ✅ `repo` (ทั้งหมด)
6. คลิก **"Generate token"**
7. **คัดลอก Token ทันที** (จะไม่แสดงอีก!)

#### 2. ใช้ Token แทนรหัสผ่าน

**วิธีที่ 1: ใส่ใน URL**
```bash
# แทนที่ YOUR_USERNAME และ YOUR_TOKEN
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/AI-Medical-System.git

# Push
git push -u origin main
```

**วิธีที่ 2: ใช้ Git Credential Helper (แนะนำ)**
```bash
# Push ตามปกติ
git push -u origin main

# เมื่อถาม Username และ Password:
Username: YOUR_USERNAME
Password: YOUR_TOKEN (วาง Token ที่คัดลอกไว้)

# Git จะจำ credential ให้
```

---

## ✅ ตรวจสอบว่า Push สำเร็จ

1. ไปที่ `https://github.com/YOUR_USERNAME/AI-Medical-System`
2. ควรเห็นไฟล์ทั้งหมดบน GitHub
3. `README.md` จะแสดงที่หน้าแรก

---

## 🚂 ขั้นตอนต่อไป: Deploy บน Railway

หลังจาก Push ขึ้น GitHub แล้ว:

1. ไปที่ [Railway](https://railway.app/)
2. Login ด้วย GitHub
3. คลิก **"New Project"**
4. เลือก **"Deploy from GitHub repo"**
5. เลือก **AI-Medical-System**
6. ตั้งค่า Environment Variables:
   - `OPENAI_API_KEY=your_api_key_here`
7. คลิก **"Deploy"**

---

## 📌 คำสั่ง Git ที่ใช้บ่อย

```bash
# ดูสถานะไฟล์
git status

# เพิ่มไฟล์ทั้งหมด
git add .

# Commit
git commit -m "Your message"

# Push
git push

# ดู remote URL
git remote -v

# เปลี่ยน remote URL
git remote set-url origin NEW_URL

# ดูประวัติ commit
git log --oneline

# ดู branch ปัจจุบัน
git branch
```

---

## 🎯 ตัวอย่างคำสั่งเต็ม (คัดลอกได้เลย)

**แทนที่ `YOUR_USERNAME` ด้วยชื่อ GitHub ของคุณก่อนรันคำสั่ง!**

```bash
# 1. ไปที่โฟลเดอร์โปรเจค
cd /Users/techit/Desktop/Login-Learning/Cource/AIForMed/AiForMed/Test/AI-Medical-System

# 2. ลบ remote เก่า
git remote remove origin

# 3. เพิ่ม remote ใหม่ (แทนที่ YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AI-Medical-System.git

# 4. ตรวจสอบ
git remote -v

# 5. เปลี่ยน branch เป็น main
git branch -M main

# 6. Push
git push -u origin main

# ถ้าถาม Username/Password ใช้ Personal Access Token
```

---

## ⚠️ ข้อควรระวัง

### 1. ไม่ควร commit ไฟล์เหล่านี้
- ✅ `.gitignore` จะป้องกันอัตโนมัติ:
  - `.env` (API Keys)
  - `*.pkl` (ML Models ขนาดใหญ่)
  - `*.csv` (Dataset)
  - `env/` (Virtual environment)

### 2. ตรวจสอบก่อน Push
```bash
# ดูว่าจะ commit อะไรบ้าง
git status

# ถ้าเห็นไฟล์ที่ไม่ควร commit ให้เพิ่มใน .gitignore
echo "filename.extension" >> .gitignore
```

### 3. ขนาด Repository
- GitHub Free: **ไม่เกิน 100 MB/file**
- Repository: **ไม่ควรเกิน 1 GB**

ตรวจสอบขนาดไฟล์:
```bash
find . -type f -size +100M
```

---

## 🎓 เรียนรู้เพิ่มเติม

- [GitHub Docs](https://docs.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

<div align="center">

**พร้อม Push ขึ้น GitHub แล้ว!** 🚀

</div>