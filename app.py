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
        return pd.read_csv("questions.csv")
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ ไม่พบไฟล์ข้อมูลข้อสอบ `questions.csv` กรุณาตรวจสอบว่าวางไว้ในโฟลเดอร์เดียวกันหรือยัง")
else:
    # เมนูด้านข้างสำหรับเลือกสัปดาห์
    st.sidebar.title("📚 เมนูบทเรียน ก.พ.")
    all_weeks = df["week"].unique()
    selected_week = st.sidebar.selectbox("เลือกสัปดาห์ที่ต้องการเรียน:", all_weeks)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 ทำข้อสอบแล้วนำคะแนนไปบันทึกลง Google Sheets แดชบอร์ดของคุณได้เลย!")

    # กรองข้อสอบเฉพาะสัปดาห์ที่เลือก
    week_data = df[df["week"] == selected_week]
    
    st.header(f"📌 {selected_week}")
    
    # ฟอร์มทำข้อสอบ
    with st.form(f"form_{selected_week}"):
        user_answers = {}
        
        # วนลูปแสดงข้อสอบทั้งหมดในสัปดาห์นั้น
        for index, row in week_data.iterrows():
            st.subheader(f"หมวด: {row['category']}")
            st.write(f"**{row['question']}**")
            
            options = (row["option_a"], row["option_b"], row["option_c"], row["option_d"])
            
            # สร้างตัวเลือก Radio
            user_answers[index] = st.radio(
                f"เลือกคำตอบ (ข้อ {index+1}):",
                options,
                key=f"q_{index}",
                label_visibility="collapsed"
            )
            st.write("") # เว้นวรรค
            
        submitted = st.form_submit_button("🏁 ส่งคำตอบและตรวจคะแนน")

    # เมื่อกดส่งคำตอบ
    if submitted:
        score = 0
        total_questions = len(week_data)
        
        for index, row in week_data.iterrows():
            if user_answers[index] == row["answer"]:
                score += 1
                
        # แสดงผลลัพธ์
        st.success(f"🎉 คุณทำคะแนนรวมได้: {score} / {total_questions} คะแนน")
        
        if score == total_questions:
            st.balloons()
            st.markdown("### 🌟 สุดยอดมาก! ได้คะแนนเต็มเลย!")
        elif score >= total_questions / 2:
            st.info("👍 ผ่านเกณฑ์ปานกลางแล้ว เก่งมากครับ!")
        else:
            st.warning("💪 สู้ๆ ครับ! ลองทบทวนเนื้อหาแล้วทำใหม่อีกรอบนะ")
            
        # แสดงเฉลย
        with st.expander("📖 ดูเฉลยละเอียด"):
            for index, row in week_data.iterrows():
                st.write(f"• **{row['question']}**")
                st.write(f"  - คำตอบที่ถูกต้อง: `{row['answer']}`")
                st.write(f"  - คำอธิบาย: {row['explanation']}")
                st.write("---")