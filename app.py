import streamlit as st
import joblib
import pandas as pd

# โหลดโมเดล
model_path = "voting_classifier_model (1).pkl"
model = joblib.load(model_path)

# กำหนดฟีเจอร์ที่ใช้
selected_features = ['age', 'sex', 'trestbps', 'chol', 'thalch', 'oldpeak']

# เปลี่ยนสีพื้นหลังและจัดสไตล์
st.markdown(
    """
    <style>
        /* เปลี่ยนสีพื้นหลัง */
        body {
            background-color: #024F55;
        }
        .stApp {
            background-color: #024F55;
        }

        /* ปรับแต่งฟอร์ม input */
        .stTextInput, .stSelectbox {
            border-radius: 10px;
            border: 1px solid #9BD8DB;
            padding: 10px;
        }

        /* ปรับแต่งปุ่ม */
        .stButton>button {
            width: 50%;
            border-radius: 10px;
            background-color: #9BD8DB;
            color: #024F55;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ส่วนหัวของแอป
st.markdown("""
    <h1 style='text-align: center; color: #9BD8DB;'>ระบบวิเคราะห์ความเสี่ยงโรคหัวใจ</h1>
    <h3 style='text-align: center; color: #F1F9FB;'>กรอกข้อมูลเพื่อทำการวิเคราะห์</h3>
""", unsafe_allow_html=True)

# ฟอร์มรับข้อมูล
with st.form("user_input"):
    col1, col2 = st.columns(2)  # แบ่งออกเป็น 2 คอลัมน์

    with col1:
        age = st.text_input("อายุ (AGE)")
        trestbps = st.text_input("ความดันโลหิตขณะพัก (TRESTBPS)")
        chol = st.text_input("ระดับคอเลสเตอรอล (CHOL)")

    with col2:
        sex = st.selectbox("เพศ (SEX)", ["หญิง (0)", "ชาย (1)"])
        thalch = st.text_input("อัตราการเต้นหัวใจสูงสุด (THALCH)")
        oldpeak = st.text_input("ST Depression (OLDPEAK)")

    # ปุ่มทำนายให้อยู่ตรงกลาง
    col_center = st.columns([1, 2, 4])  # จัดให้ตรงกลาง
    with col_center[2]:  
        submitted = st.form_submit_button("ทำนายผล")

if submitted:
    try:
        # จัดการค่าที่รับมา
        user_inputs = {
            'age': age,
            'sex': 0 if sex == "หญิง (0)" else 1,
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

        st.write("**ข้อมูลอินพุตที่ใช้ทำนาย:**", user_data)

        # ทำนายผล
        prediction = model.predict(user_data)
        result = "⚠️ มีความเสี่ยงเป็นโรคหัวใจ" if prediction[0] == 1 else "✅ ไม่มีความเสี่ยงเป็นโรคหัวใจ"
        st.success(f"🔹 **ผลลัพธ์:** {result}")

    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")
