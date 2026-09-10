import streamlit as st
from datetime import datetime

# ตั้งค่าหน้าตาเบื้องต้นของเว็บ
st.set_page_config(page_title="ระบบจองคิวร้านตัดผม", page_icon="✂️", layout="wide")

# ---------------------------------------------------------
# จำลองฐานข้อมูลเก็บรายการจอง (ใช้ session_state)
# ---------------------------------------------------------
if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "queue_number" not in st.session_state:
    st.session_state.queue_number = 1

# ---------------------------------------------------------
# เมนูหลักด้านซ้าย (Sidebar)
# ---------------------------------------------------------
st.sidebar.title("💈 เมนูหลัก")
menu = st.sidebar.radio(
    "เลือกเมนูที่ต้องการ",
    [
        "1. จองคิว / กรอกข้อมูล (ข้อ 2, 3, 4, 5)",
        "2. ตรวจสอบคิว / ยกเลิกคิว (ข้อ 6)",
        "3. ข้อมูลร้าน / ช่างตัดผม (ข้อ 7)",
        "4. ระบบหลังร้าน [สำหรับเจ้าของร้าน] (ข้อ 1)"
    ]
)

# รายชื่อช่างในร้าน
stylists = [
    "ช่างคนไหนก็ได้ (ไม่ระบุ)",
    "ช่างเอก (ผู้เชี่ยวชาญทรงผมชาย/วินเทจ)",
    "ช่างแอน (ผู้เชี่ยวชาญดัด/ทำสี/ทรงผมหญิง)",
    "ช่างใหม่ (ผู้เชี่ยวชาญสระ-ไดร์/เซ็ตทรงเกาหลี)"
]

# =========================================================
# เมนู 1: จองคิว / กรอกข้อมูลลูกค้า / เลือกช่าง / แสดงหมายเลขคิว
# =========================================================
if menu == "1. จองคิว / กรอกข้อมูล (ข้อ 2, 3, 4, 5)":
    st.title("✂️ บริการจองคิวออนไลน์")
    st.caption("กรุณากรอกข้อมูลด้านล่างให้ครบถ้วนเพื่อรับหมายเลขคิว")

    with st.form("booking_form"):
        st.subheader("📝 1. ข้อมูลลูกค้า")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("ชื่อ-นามสกุล ผู้จอง *")
            phone = st.text_input("เบอร์โทรศัพท์ *", max_chars=10)
        with col2:
            note = st.text_input("หมายเหตุ / คำขอเพิ่มเติม (ถ้ามี)")

        st.subheader("💈 2. ข้อมูลบริการและช่าง")
        col3, col4 = st.columns(2)
        with col3:
            service = st.selectbox(
                "เลือกบริการ", 
                ["ตัดผมชาย", "ตัดผมหญิง", "สระ-ไดร์", "ทำสีผม", "ดัดผม/ยืดผม", "สปาผม"]
            )
            # ข้อ 2: เลือกช่างได้
            stylist = st.selectbox("เลือกช่างตัดผม", stylists)
        
        with col4:
            date = st.date_input("วันที่ต้องการเข้าใช้บริการ", min_value=datetime.today())
            time = st.time_input("เวลาที่สะดวก")

        submitted = st.form_submit_button("🚀 ยืนยันการจองคิว")

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("⚠️ กรุณากรอกชื่อและเบอร์โทรศัพท์ให้ครบถ้วน")
            elif not phone.isdigit() or len(phone) < 9:
                st.error("⚠️ กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง")
            else:
                # สร้างรหัสคิว เช่น Q001, Q002
                q_code = f"Q{st.session_state.queue_number:03d}"
                st.session_state.queue_number += 1

                booking_info = {
                    "queue_code": q_code,
                    "name": name,
                    "phone": phone,
                    "service": service,
                    "stylist": stylist,
                    "date": str(date),
                    "time": str(time),
                    "note": note if note else "-",
                    "status": "รอรับบริการ"
                }
                st.session_state.bookings.append(booking_info)
                
                # ข้อ 5: แสดงหมายเลขคิว
                st.balloons()
                st.success("🎉 จองคิวสำเร็จแล้ว!")
                st.markdown(f"### 🎫 หมายเลขคิวของคุณคือ: **`{q_code}`**")
                st.info(f"**คุณ:** {name} | **ช่าง:** {stylist} | **วัน-เวลา:** {date} @ {time}")

# =========================================================
# เมนู 2: ตรวจสอบคิว / ยกเลิกคิว (ข้อ 6)
# =========================================================
elif menu == "2. ตรวจสอบคิว / ยกเลิกคิว (ข้อ 6)":
    st.title("🔍 ตรวจสอบและยกเลิกคิว")
    
    search_input = st.text_input("พิมพ์ 'หมายเลขคิว (เช่น Q001)' หรือ 'เบอร์โทรศัพท์' เพื่อค้นหา")
    
    if search_input:
        found = False
        for idx, b in enumerate(st.session_state.bookings):
            if search_input.strip().lower() in b['queue_code'].lower() or search_input.strip() in b['phone']:
                found = True
                st.success(f"พบข้อมูลคิว: {b['queue_code']}")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**ชื่อผู้จอง:** {b['name']}")
                    st.write(f"**เบอร์โทร:** {b['phone']}")
                    st.write(f"**บริการ:** {b['service']} | **ช่าง:** {b['stylist']}")
                    st.write(f"**วัน-เวลา:** {b['date']} เวลา {b['time']}")
                    st.write(f"**สถานะ:** `{b['status']}`")
                
                with col2:
                    if b['status'] != "ยกเลิกแล้ว":
                        # ปุ่มยกเลิกคิว
                        if st.button("❌ ยกเลิกคิวนี้", key=f"cancel_{idx}"):
                            st.session_state.bookings[idx]['status'] = "ยกเลิกแล้ว"
                            st.warning("ยกเลิกคิวเรียบร้อยแล้ว")
                            st.rerun()
                    else:
                        st.error("คิวนี้ถูกยกเลิกแล้ว")
                st.divider()
        if not found:
            st.warning("ไม่พบข้อมูลคิวจากคำค้นหาของคุณ")
            
    st.subheader("📋 คิวทั้งหมดในระบบวันนี้")
    if st.session_state.bookings:
        for b in st.session_state.bookings:
            st.write(f"• **[{b['queue_code']}]** คุณ {b['name']} - ช่าง: {b['stylist']} | เวลา: {b['time']} | สถานะ: `{b['status']}`")
    else:
        st.info("ยังไม่มีรายการคิวในขณะนี้")

# =========================================================
# เมนู 3: ดูข้อมูลร้าน (ข้อ 7)
# =========================================================
elif menu == "3. ข้อมูลร้าน / ช่างตัดผม (ข้อ 7)":
    st.title("💈 ข้อมูลร้านตัดผม & ช่างประจำร้าน")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 ที่ตั้งและเวลาทำการ")
        st.write("**ชื่อร้าน:** Barber & Salon Style")
        st.write("**เวลาเปิด-ปิด:** 10:00 น. - 20:00 น. (เปิดบริการทุกวัน)")
        st.write("**ที่อยู่:** 123/45 ถนนสายหลัก ต.ในเมือง อ.เมือง")
        st.write("**เบอร์ติดต่อร้าน:** 081-234-5678")
        st.write("**Line Official:** @barbershop")
        
    with col2:
        st.subheader("อัตราค่าบริการเริ่มต้น")
        st.write("• ตัดผมชาย: 150 - 250 บาท")
        st.write("• ตัดผมหญิง: 250 - 400 บาท")
        st.write("• สระ-ไดร์: 120 บาท")
        st.write("• ทำสีผม / ดัดผม: เริ่มต้น 800 บาท")

    st.divider()
    st.subheader("✂️ ช่างประจำร้านของเรา")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 👨‍🎤 ช่างเอก")
        st.write("เชี่ยวชาญทรงผมชาย วินเทจ แกะลาย และทรงแฟชั่นชาย")
    with c2:
        st.markdown("### 👩‍🎤 ช่างแอน")
        st.write("เชี่ยวชาญการตัดแต่งทรงผมหญิง ทำสีแฟชั่น ยืด/ดัดดิจิตอล")
    with c3:
        st.markdown("### 🧑‍🎤 ช่างใหม่")
        st.write("เชี่ยวชาญการสระนวดผ่อนคลาย เซ็ตทรงสไตล์เกาหลี")

# =========================================================
# เมนู 4: ระบบหลังร้าน (ข้อ 1)
# =========================================================
elif menu == "4. ระบบหลังร้าน [สำหรับเจ้าของร้าน] (ข้อ 1)":
    st.title("⚙️ ระบบบริหารจัดการหลังร้าน")
    
    # ระบบล็อกอินเข้าหลังร้าน
    password = st.sidebar.text_input("ใส่รหัสผ่านหลังร้าน", type="password")
    
    # รหัสผ่านคือ 1234
    if password == "1234":
        st.success("🔓 เข้าสู่ระบบหลังร้านสำเร็จ")
        
        # สรุปสถิติจำนวนคิว
        total = len(st.session_state.bookings)
        waiting = len([b for b in st.session_state.bookings if b['status'] == "รอรับบริการ"])
        done = len([b for b in st.session_state.bookings if b['status'] == "บริการเสร็จสิ้น"])
        
        m1, m2, m3 = st.columns(3)
        m1.metric("คิวทั้งหมด", total)
        m2.metric("กำลังรอคิว", waiting)
        m3.metric("เสร็จสิ้นแล้ว", done)
        
        st.divider()
        st.subheader("📑 รายการคิวลูกค้าทั้งหมด")
        
        if st.session_state.bookings:
            for idx, b in enumerate(st.session_state.bookings):
                with st.expander(f"🎫 คิว {b['queue_code']}: คุณ {b['name']} ({b['phone']}) - ช่าง {b['stylist']}"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.write(f"**บริการ:** {b['service']}")
                        st.write(f"**วัน-เวลา:** {b['date']} @ {b['time']}")
                        st.write(f"**หมายเหตุ:** {b['note']}")
                    with c2:
                        # เจ้าของร้านเปลี่ยนสถานะคิวได้
                        new_status = st.selectbox(
                            "อัปเดตสถานะคิว",
                            ["รอรับบริการ", "กำลังใช้บริการ", "บริการเสร็จสิ้น", "ยกเลิกแล้ว"],
                            key=f"status_admin_{idx}",
                            index=["รอรับบริการ", "กำลังใช้บริการ", "บริการเสร็จสิ้น", "ยกเลิกแล้ว"].index(b['status'])
                        )
                        st.session_state.bookings[idx]['status'] = new_status
                    with c3:
                        # เจ้าของร้านลบคิวออกจากระบบได้
                        if st.button("🗑️ ลบคิวนี้ออกจากฐานข้อมูล", key=f"del_admin_{idx}"):
                            st.session_state.bookings.pop(idx)
                            st.rerun()
                            
            if st.button("🔴 ล้างข้อมูลคิวทั้งหมดในระบบ"):
                st.session_state.bookings = []
                st.rerun()
        else:
            st.info("ไม่มีรายการคิวในระบบ")
    else:
        st.warning("🔒 กรุณากรอกรหัสผ่านที่แถบเมนูด้านซ้ายเพื่อเข้าใช้งานหลังร้าน (รหัสผ่านเริ่มต้น: 1234)")
