import streamlit as st
import joblib
import pandas as pd

# โหลดโมเดล
model_path = "voting_classifier_model (1).pkl"
model = joblib.load(model_path)

# กำหนดฟีเจอร์ที่ใช้
selected_features = ['age', 'sex', 'trestbps', 'chol', 'thalch', 'oldpeak']

st.markdown("""
    <h1 style='text-align: center; color: #d90429;'>❤️ ระบบวิเคราะห์ความเสี่ยงโรคหัวใจ ❤️</h1>
    <h3 style='text-align: center; color: #ff6b6b;'>กรอกข้อมูลเพื่อทำการวิเคราะห์</h3>
""", unsafe_allow_html=True)

with st.form("user_input"):
    col1, col2 = st.columns(2)  # แบ่งเป็น 2 คอลัมน์

    with col1:
        sex = st.selectbox("เพศ : SEX", ["หญิง (0)", "ชาย (1)"])  # ให้เลือกเพศ
        age = st.text_input("อายุ : AGE")  # ให้พิมพ์อายุ
        trestbps = st.text_input("ความดันโลหิตขณะพัก : TRESTBPS")  # ให้พิมพ์ความดันโลหิตขณะพัก
        chol = st.text_input("ระดับคอเลสเตอรอล : CHOL")  # ให้พิมพ์คอเลสเตอรอล


    with col2:
        thalch = st.text_input("อัตราการเต้นหัวใจสูงสุด : THALCH")  # ให้พิมพ์อัตราการเต้นหัวใจสูงสุด
        oldpeak = st.text_input("ST Depression : OLDPEAK")  # ให้พิมพ์ระดับ ST Depression

    submitted = st.form_submit_button("ทำนายผล")  # Submit button

if submitted:
    try:
        # แปลงค่าจากอินพุตให้เป็นตัวเลข
        user_inputs = {
            'age': age,
            'sex': 0 if sex == "หญิง (0)" else 1,  # แปลงเพศเป็น 0 หรือ 1
            'trestbps': trestbps,
            'chol': chol,
            'thalch': thalch,
            'oldpeak': oldpeak
        }

        # ตรวจสอบค่าที่กรอกเข้ามาว่าถูกต้องหรือไม่
        for key, value in user_inputs.items():
            if key != 'sex' and (value == "" or not value.replace(".", "", 1).isdigit()):
                st.warning(f"⚠️ กรุณากรอกค่าที่ถูกต้องสำหรับ {key}")
                st.stop()

        # แปลงข้อมูลจาก input ให้เป็นตัวเลข
        user_inputs = {key: float(value) if key != 'sex' else value for key, value in user_inputs.items()}

        # สร้าง DataFrame
        user_data = pd.DataFrame([user_inputs], columns=selected_features)

        st.write("ข้อมูลอินพุตที่ใช้ทำนาย:", user_data)

        # ทำนายผล
        prediction = model.predict(user_data)
        result = "มีความเสี่ยงเป็นโรคหัวใจ" if prediction[0] == 1 else "ไม่มีความเสี่ยงเป็นโรคหัวใจ"
        st.success(f"🔹 ผลลัพธ์: {result}")

    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")
