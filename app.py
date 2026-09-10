if "bookings" not in st.session_state:
    st.session_state.bookings = []

# ฟอร์มรับข้อมูลการจอง
with st.form("booking_form"):
    name = st.text_input("ชื่อผู้จอง")
    service = st.selectbox("เลือกบริการ", ["ตัดผมชาย", "ตัดผมหญิง", "สระ-ไดร์", "ทำสีผม"])
    date = st.date_input("วันที่ต้องการจอง", min_value=datetime.today())
    time = st.time_input("เวลาที่ต้องการจอง")
    
    submitted = st.form_submit_button("ยืนยันการจอง")
    
    if submitted:
        if name.strip() == "":
            st.error("กรุณากรอกชื่อผู้จอง")
        else:
            booking_info = {
                "name": name,
                "service": service,
                "date": str(date),
                "time": str(time)
            }
            st.session_state.bookings.append(booking_info)
            st.success(f"จองคิวสำเร็จแล้วสำหรับคุณ {name}!")

# แสดงรายการคิวที่ถูกจองแล้ว
st.divider()
st.subheader("📋 รายการคิวที่จองแล้ว")

if st.session_state.bookings:
    for idx, b in enumerate(st.session_state.bookings, 1):
        st.write(f"**{idx}. คุณ {b['name']}** - บริการ: {b['service']} | วันที่: {b['date']} เวลา: {b['time']}")
else:
    st.info("ยังไม่มีข้อมูลการจองในขณะนี้")
