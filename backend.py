# backend.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from PIL import Image
import io
import os
from dotenv import load_dotenv
import pandas as pd
from typing import Optional, List, Dict
import json
import pickle
from datetime import datetime

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

# ML imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# โหลด AI Models
xray_model = YOLO("models/xray_best.pt")
blood_model = YOLO("models/blood_best.pt")

# LangChain Chatbot Setup
# Set environment variable for OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.3
)

# เก็บ memory สำหรับแต่ละ session
chat_memories = {}

# เก็บข้อมูลการซักประวัติอาการ
symptom_sessions = {}

# โหลดข้อมูลผู้ป่วย
try:
    patient_df = pd.read_csv("healthcare_dataset.csv")
    patient_df.columns = patient_df.columns.str.strip()
    print(f"โหลดข้อมูลผู้ป่วย {len(patient_df)} รายการ")
except Exception as e:
    print(f"ไม่สามารถโหลดข้อมูลผู้ป่วย: {e}")
    patient_df = None

# สร้างและฝึก ML model สำหรับทำนายอาการ
def train_condition_prediction_model():
    """ฝึกโมเดลทำนายอาการจากข้อมูลผู้ป่วย"""
    global patient_df, condition_model, label_encoders

    if patient_df is None:
        print("ไม่สามารถฝึกโมเดล: ไม่มีข้อมูลผู้ป่วย")
        return None

    try:
        # เตรียมข้อมูล
        df_model = patient_df.copy()

        # เลือก features ที่จะใช้
        feature_columns = ['Age', 'Gender', 'Blood Type', 'Test Results']
        target_column = 'Medical Condition'

        # Encode categorical variables
        label_encoders = {}
        for col in ['Gender', 'Blood Type', 'Test Results']:
            le = LabelEncoder()
            df_model[col] = le.fit_transform(df_model[col].astype(str))
            label_encoders[col] = le

        # Encode target
        le_target = LabelEncoder()
        df_model[target_column] = le_target.fit_transform(df_model[target_column])
        label_encoders['target'] = le_target

        # แบ่งข้อมูล
        X = df_model[feature_columns]
        y = df_model[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # ฝึกโมเดล
        condition_model = RandomForestClassifier(n_estimators=100, random_state=42)
        condition_model.fit(X_train, y_train)

        # ทดสอบความแม่นยำ
        y_pred = condition_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"โมเดลทำนายอาการ - ความแม่นยำ: {accuracy:.2%}")

        # บันทึกโมเดล
        with open('condition_model.pkl', 'wb') as f:
            pickle.dump({'model': condition_model, 'encoders': label_encoders}, f)

        return condition_model

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการฝึกโมเดล: {e}")
        return None

# ฝึกโมเดลเมื่อเริ่มต้นระบบ
condition_model = train_condition_prediction_model()

def get_symptom_questions():
    """คำถามสำหรับซักประวัติอาการ"""
    return [
        {"key": "age", "question": "อายุของคุณเท่าไหร่ครับ/ค่ะ?", "type": "number"},
        {"key": "gender", "question": "เพศของคุณคือ?", "type": "choice",
         "options": ["ชาย", "หญิง"], "values": ["Male", "Female"]},
        {"key": "blood_type", "question": "กรุ๊ปเลือดของคุณคือ?", "type": "choice",
         "options": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},
        {"key": "symptoms", "question": "อาการหลักที่คุณมีคืออะไร? (เช่น ปวดหัว, เจ็บหน้าอก, หายใจลำบาก)", "type": "text"},
        {"key": "duration", "question": "มีอาการมานานแค่ไหน? (เช่น 2 วัน, 1 สัปดาห์)", "type": "text"},
        {"key": "severity", "question": "ความรุนแรงของอาการ 1-10? (1=เล็กน้อย, 10=รุนแรงมาก)", "type": "number"},
        {"key": "test_result", "question": "เคยตรวจเลือดล่าสุดผลเป็นอย่างไร?", "type": "choice",
         "options": ["ปกติ", "ผิดปกติ", "ไม่แน่ใจ"], "values": ["Normal", "Abnormal", "Inconclusive"]}
    ]

def predict_medical_condition(age, gender, blood_type, test_result="Inconclusive"):
    """ทำนายอาการจากข้อมูลผู้ป่วย"""
    global condition_model, label_encoders

    if condition_model is None:
        return None

    try:
        # แปลงภาษาไทยเป็นภาษาอังกฤษ
        gender_map = {"ชาย": "Male", "หญิง": "Female", "Male": "Male", "Female": "Female"}
        test_map = {"ปกติ": "Normal", "ผิดปกติ": "Abnormal", "ไม่แน่ใจ": "Inconclusive",
                   "Normal": "Normal", "Abnormal": "Abnormal", "Inconclusive": "Inconclusive"}

        gender = gender_map.get(gender, "Male")
        test_result = test_map.get(test_result, "Inconclusive")

        # ตรวจสอบว่า label อยู่ใน encoder หรือไม่
        if gender not in label_encoders['Gender'].classes_:
            print(f"Unknown gender: {gender}, using Male")
            gender = "Male"

        if blood_type not in label_encoders['Blood Type'].classes_:
            print(f"Unknown blood type: {blood_type}, using O+")
            blood_type = "O+"

        if test_result not in label_encoders['Test Results'].classes_:
            print(f"Unknown test result: {test_result}, using Inconclusive")
            test_result = "Inconclusive"

        # เตรียมข้อมูลสำหรับทำนาย
        input_data = pd.DataFrame({
            'Age': [age],
            'Gender': [label_encoders['Gender'].transform([gender])[0]],
            'Blood Type': [label_encoders['Blood Type'].transform([blood_type])[0]],
            'Test Results': [label_encoders['Test Results'].transform([test_result])[0]]
        })

        # ทำนาย
        prediction = condition_model.predict(input_data)[0]
        probabilities = condition_model.predict_proba(input_data)[0]

        # แปลงผลลัพธ์
        predicted_condition = label_encoders['target'].inverse_transform([prediction])[0]

        # หาความน่าจะเป็นของแต่ละอาการ
        condition_probs = {}
        for idx, prob in enumerate(probabilities):
            condition_name = label_encoders['target'].inverse_transform([idx])[0]
            condition_probs[condition_name] = float(prob)

        # เรียงลำดับตามความน่าจะเป็น
        sorted_probs = dict(sorted(condition_probs.items(), key=lambda x: x[1], reverse=True))

        return {
            "predicted_condition": predicted_condition,
            "confidence": float(max(probabilities)),
            "probabilities": sorted_probs
        }

    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

def get_medical_system_prompt():
    """System prompt สำหรับ Medical Chatbot"""
    return """คุณเป็น AI ผู้ช่วยทางการแพทย์ที่เชี่ยวชาญ มีหน้าที่:

1. ตอบคำถามเกี่ยวกับสุขภาพและการแพทย์
2. ซักประวัติอาการอย่างละเอียด
3. ทำนายโรคที่เป็นไปได้จากอาการและข้อมูล
4. อธิบายผลการตรวจทางการแพทย์
5. แนะนำการดูแลสุขภาพ
6. ค้นหาและให้ข้อมูลผู้ป่วยจากฐานข้อมูล

เมื่อผู้ใช้บอกว่ามีอาการไม่สบาย:
- ให้ซักถามตามลำดับคำถามที่กำหนด
- รวบรวมข้อมูลให้ครบก่อนทำนาย
- ใช้ระบบ ML ทำนายอาการที่เป็นไปได้
- แนะนำให้พบแพทย์เสมอ

ข้อสำคัญ:
- เตือนให้ปรึกษาแพทย์เสมอ
- ไม่ให้การวินิจฉัยขาด
- ตอบเป็นภาษาไทยที่เข้าใจง่าย
- เป็นมิตรและให้กำลังใจ
- รักษาความเป็นส่วนตัวของข้อมูลผู้ป่วย

ตอบสั้นๆ กระชับ ไม่เกิน 3-4 ประโยค"""

def search_patient_data(query: str, max_results: int = 5) -> str:
    """ค้นหาข้อมูลผู้ป่วยสำหรับ chatbot"""
    if patient_df is None:
        return "ไม่สามารถเข้าถึงข้อมูลผู้ป่วยได้"

    try:
        # ค้นหาจากชื่อ
        name_results = patient_df[patient_df['Name'].str.contains(query, case=False, na=False)]

        # ค้นหาจากอาการ
        condition_results = patient_df[patient_df['Medical Condition'].str.contains(query, case=False, na=False)]

        # รวมผลลัพธ์
        results = pd.concat([name_results, condition_results]).drop_duplicates()
        results = results.head(max_results)

        if len(results) == 0:
            return f"ไม่พบข้อมูลผู้ป่วยที่เกี่ยวข้องกับ '{query}'"

        # สร้างข้อความสรุป
        summary = f"พบข้อมูลผู้ป่วย {len(results)} ราย:\n"
        for idx, row in results.iterrows():
            summary += f"\n- {row['Name']}: อายุ {row['Age']} ปี, {row['Gender']}, "
            summary += f"กรุ๊ปเลือด {row['Blood Type']}, อาการ: {row['Medical Condition']}, "
            summary += f"แพทย์: {row['Doctor']}, โรงพยาบาล: {row['Hospital']}"

        return summary

    except Exception as e:
        return f"เกิดข้อผิดพลาดในการค้นหาข้อมูล: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the index.html file"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return {"message": "AI Medical API + Chatbot Ready! 🏥🤖"}

@app.get("/api")
def api_home():
    """API health check endpoint"""
    return {"message": "AI Medical API + Chatbot Ready! 🏥🤖", "status": "online"}

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    image_type: str = Form(...)
):
    """วิเคราะห์ภาพทางการแพทย์ (เดิม)"""
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    if image_type == "xray":
        results = xray_model(image)
        if results[0].probs:
            probs = results[0].probs.data.cpu().numpy()
            classes = xray_model.names
            
            best_idx = probs.argmax()
            best_class = classes[best_idx]
            confidence = float(probs[best_idx])
            
            return {
                "type": "xray",
                "result": best_class,
                "confidence": f"{confidence:.1%}",
                "success": True
            }
    
    elif image_type == "blood":
        results = blood_model(image)
        if results[0].boxes:
            boxes = results[0].boxes
            cell_counts = {}
            
            for box in boxes:
                cls_id = int(box.cls)
                class_name = blood_model.names[cls_id]
                cell_counts[class_name] = cell_counts.get(class_name, 0) + 1
            
            return {
                "type": "blood",
                "cell_counts": cell_counts,
                "total_cells": len(boxes),
                "success": True
            }
    
    return {"error": "Analysis failed", "success": False}

@app.post("/symptom/start")
async def start_symptom_tracking(session_id: str = Form(default="default")):
    """เริ่มการซักประวัติอาการ"""
    symptom_sessions[session_id] = {
        "answers": {},
        "questions": get_symptom_questions(),
        "current_index": 0,
        "started_at": datetime.now().isoformat()
    }

    first_question = symptom_sessions[session_id]["questions"][0]
    return {
        "session_id": session_id,
        "question": first_question["question"],
        "question_key": first_question["key"],
        "question_type": first_question["type"],
        "options": first_question.get("options"),
        "progress": f"1/{len(get_symptom_questions())}",
        "success": True
    }

@app.post("/symptom/answer")
async def submit_symptom_answer(
    session_id: str = Form(...),
    question_key: str = Form(...),
    answer: str = Form(...)
):
    """บันทึกคำตอบและถามคำถามถัดไป"""
    if session_id not in symptom_sessions:
        return {"error": "Session not found", "success": False}

    session = symptom_sessions[session_id]

    # บันทึกคำตอบ
    session["answers"][question_key] = answer
    session["current_index"] += 1

    # ตรวจสอบว่ายังมีคำถามอีกไหม
    if session["current_index"] < len(session["questions"]):
        next_question = session["questions"][session["current_index"]]
        return {
            "session_id": session_id,
            "question": next_question["question"],
            "question_key": next_question["key"],
            "question_type": next_question["type"],
            "options": next_question.get("options"),
            "progress": f"{session['current_index'] + 1}/{len(session['questions'])}",
            "success": True
        }
    else:
        # ถามครบแล้ว ทำนายผล
        answers = session["answers"]

        # ทำนายอาการ
        prediction = predict_medical_condition(
            age=int(answers.get("age", 30)),
            gender=answers.get("gender", "Male"),
            blood_type=answers.get("blood_type", "O+"),
            test_result=answers.get("test_result", "Inconclusive")
        )

        # สร้างคำแนะนำ
        if prediction:
            top_conditions = list(prediction["probabilities"].items())[:3]
            recommendation = f"""
### ผลการประเมินเบื้องต้น:
- **โรคที่มีความเป็นไปได้สูงสุด**: {prediction['predicted_condition']} ({prediction['confidence']:.1%})
- **ความเป็นไปได้อื่นๆ**:
  1. {top_conditions[0][0]}: {top_conditions[0][1]:.1%}
  2. {top_conditions[1][0]}: {top_conditions[1][1]:.1%}
  3. {top_conditions[2][0]}: {top_conditions[2][1]:.1%}

### ข้อมูลที่ได้รับ:
- อายุ: {answers.get('age')} ปี
- เพศ: {answers.get('gender')}
- กรุ๊ปเลือด: {answers.get('blood_type')}
- อาการ: {answers.get('symptoms')}
- ระยะเวลา: {answers.get('duration')}
- ความรุนแรง: {answers.get('severity')}/10

### คำแนะนำ:
⚠️ **นี่เป็นเพียงการประเมินเบื้องต้น กรุณาพบแพทย์เพื่อการวินิจฉัยที่แม่นยำ**
"""
        else:
            recommendation = "ไม่สามารถทำนายได้ กรุณาปรึกษาแพทย์"

        # ลบ session
        del symptom_sessions[session_id]

        return {
            "session_id": session_id,
            "completed": True,
            "prediction": prediction,
            "recommendation": recommendation,
            "success": True
        }

@app.post("/chat")
async def chat_with_ai(
    message: str = Form(...),
    session_id: str = Form(default="default"),
    analysis_context: str = Form(default="")
):
    """Chatbot endpoint ใหม่"""

    try:
        # สร้าง memory สำหรับ session
        if session_id not in chat_memories:
            chat_memories[session_id] = ConversationBufferMemory(return_messages=True)

        memory = chat_memories[session_id]

        # ตรวจสอบคำสำคัญเกี่ยวกับอาการไม่สบาย
        symptom_keywords = ["ไม่สบาย", "ปวด", "เจ็บ", "เป็นไข้", "อาการ", "ป่วย", "sick", "pain", "hurt",
                           "fever", "ทำนาย", "วิเคราะห์อาการ", "ตรวจอาการ"]

        # ถ้าพูดถึงอาการไม่สบาย แนะนำให้เริ่มซักประวัติ
        if any(keyword in message.lower() for keyword in symptom_keywords):
            symptom_prompt = f"""
ผู้ใช้แจ้งว่า: {message}

แนะนำให้ใช้ระบบซักประวัติอาการ โดยบอกว่า:
'ฉันสามารถช่วยซักประวัติและทำนายอาการเบื้องต้นได้
กรุณาเริ่มการซักประวัติโดยใช้ปุ่ม "เริ่มซักประวัติอาการ"
หรือถ้าต้องการให้ฉันช่วยตอบคำถามทั่วไปก็สามารถถามมาได้เลยครับ/ค่ะ'
"""
            full_prompt = get_medical_system_prompt() + symptom_prompt
        else:
            # ตรวจสอบว่าข้อความเกี่ยวกับผู้ป่วยหรือไม่
            patient_context = ""
            keywords = ["ผู้ป่วย", "คนไข้", "patient", "ชื่อ", "name", "diabetes", "cancer",
                       "asthma", "obesity", "arthritis", "hypertension", "เบาหวาน", "มะเร็ง",
                       "หืด", "อ้วน", "ข้อเอื้อม", "ความดัน"]

            # ถ้ามีคำเกี่ยวกับผู้ป่วย ให้ค้นหาข้อมูล
            if any(keyword in message.lower() for keyword in keywords):
                # ดึงคำค้นหาจากข้อความ
                search_terms = []
                for word in message.split():
                    if len(word) > 2:  # คำที่ยาวกว่า 2 ตัวอักษร
                        search_terms.append(word)

                # ค้นหาข้อมูลผู้ป่วย
                for term in search_terms[:3]:  # ค้นหาแค่ 3 คำแรก
                    patient_info = search_patient_data(term, max_results=3)
                    if "พบข้อมูลผู้ป่วย" in patient_info:
                        patient_context = f"\n\n### ข้อมูลผู้ป่วยจากฐานข้อมูล:\n{patient_info}\n"
                        break

            # สร้าง context จากผลการวิเคราะห์ (ถ้ามี)
            context_prompt = ""
            if analysis_context:
                context_prompt = f"\n\nบริบทจากการวิเคราะห์ภาพล่าสุด: {analysis_context}\n"

            # สร้าง full prompt
            full_prompt = get_medical_system_prompt() + patient_context + context_prompt + f"\n\nคำถาม: {message}"

        # ได้ประวัติการสนทนา
        chat_history = memory.chat_memory.messages

        # สร้าง messages สำหรับ LangChain
        messages = [HumanMessage(content=full_prompt)]

        # เพิ่มประวัติการสนทนา (เฉพาะ 5 ข้อความล่าสุด)
        if chat_history:
            recent_history = chat_history[-5:]  # เอาแค่ 5 ข้อความล่าสุด
            messages = recent_history + messages

        # เรียก LangChain
        response = llm.invoke(messages)
        ai_response = response.content

        # บันทึกลง memory
        memory.chat_memory.add_user_message(message)
        memory.chat_memory.add_ai_message(ai_response)

        return {
            "response": ai_response,
            "session_id": session_id,
            "success": True
        }

    except Exception as e:
        return {
            "error": f"Chatbot error: {str(e)}",
            "success": False
        }

@app.post("/patient/search")
async def search_patient(
    search_query: str = Form(...),
    search_type: str = Form(default="name")
):
    """ค้นหาข้อมูลผู้ป่วย"""
    try:
        if patient_df is None:
            return {"error": "ไม่สามารถโหลดข้อมูลผู้ป่วย", "success": False}

        # ค้นหาตามประเภท
        if search_type == "name":
            results = patient_df[patient_df['Name'].str.contains(search_query, case=False, na=False)]
        elif search_type == "condition":
            results = patient_df[patient_df['Medical Condition'].str.contains(search_query, case=False, na=False)]
        elif search_type == "blood_type":
            results = patient_df[patient_df['Blood Type'] == search_query.upper()]
        else:
            results = patient_df[patient_df['Name'].str.contains(search_query, case=False, na=False)]

        # จำกัดผลลัพธ์ 10 รายการ
        results = results.head(10)

        if len(results) == 0:
            return {
                "message": "ไม่พบข้อมูลผู้ป่วยที่ค้นหา",
                "results": [],
                "success": True
            }

        # แปลงเป็น dict
        patient_list = results.to_dict('records')

        return {
            "results": patient_list,
            "total": len(results),
            "success": True
        }

    except Exception as e:
        return {
            "error": f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}",
            "success": False
        }

@app.get("/patient/stats")
async def get_patient_stats():
    """สถิติข้อมูลผู้ป่วย"""
    try:
        if patient_df is None:
            return {"error": "ไม่สามารถโหลดข้อมูลผู้ป่วย", "success": False}

        stats = {
            "total_patients": len(patient_df),
            "conditions": patient_df['Medical Condition'].value_counts().to_dict(),
            "blood_types": patient_df['Blood Type'].value_counts().to_dict(),
            "gender": patient_df['Gender'].value_counts().to_dict(),
            "avg_age": float(patient_df['Age'].mean()),
            "avg_billing": float(patient_df['Billing Amount'].mean()),
            "admission_types": patient_df['Admission Type'].value_counts().to_dict()
        }

        return {
            "stats": stats,
            "success": True
        }

    except Exception as e:
        return {
            "error": f"เกิดข้อผิดพลาดในการคำนวณสถิติ: {str(e)}",
            "success": False
        }

@app.get("/chat/clear/{session_id}")
def clear_chat_history(session_id: str):
    """ลบประวัติการสนทนา"""
    if session_id in chat_memories:
        del chat_memories[session_id]
    return {"message": f"Chat history cleared for {session_id}"}

# รันเซิร์ฟเวอร์
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)