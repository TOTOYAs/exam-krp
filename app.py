import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบเตรียมสอบ ก.พ. ภาค ก. (Data-Driven)",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 ระบบทำแบบฝึกหัด ก.พ. (Interactive Quiz)")
st.write("📚 ระบบข้อสอบออนไลน์รองรับทุกสัปดาห์ (โหลดข้อมูลจากไฟล์กลางอัตโนมัติ)")
st.write("---")

# โหลดข้อมูลข้อสอบจากไฟล์ CSV กลาง
@st.cache_data
def load_data():
    try:
        # เพิ่ม encoding="utf-8" และ on_bad_lines='skip' เพื่อป้องกัน Error
        return pd.read_csv("questions.csv", encoding="utf-8", on_bad_lines='skip')
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ CSV ได้: {e}")
        return None

df = load_data()
# ==========================================

if df is None:
    st.error("⚠️ ไม่พบไฟล์ข้อมูลข้อสอบ `questions.csv` กรุณาตรวจสอบว่าวางไว้ในโฟลเดอร์เดียวกันหรือยัง")
else: