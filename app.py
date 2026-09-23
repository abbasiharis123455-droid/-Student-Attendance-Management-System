import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import datetime

st.set_page_config(page_title="Student Attendance System", layout="centered")
st.title("📚 Student Attendance Management System")
st.markdown("---")

# Sidebar
menu = st.sidebar.selectbox("Menu", ["Mark Attendance", "Add Student", "View Records"])

if 'students' not in st.session_state:
    st.session_state.students = pd.DataFrame(columns=["ID", "Name", "Department"])
if 'attendance' not in st.session_state:
    st.session_state.attendance = pd.DataFrame(columns=["ID", "Name", "Date", "Time", "Status"])

if menu == "Add Student":
    st.header("Add New Student")
    s_id = st.text_input("Student ID")
    s_name = st.text_input("Student Name")
    s_dept = st.text_input("Department")
    if st.button("Add Student"):
        if s_id and s_name:
            new = pd.DataFrame([[s_id, s_name, s_dept]], columns=["ID", "Name", "Department"])
            st.session_state.students = pd.concat([st.session_state.students, new], ignore_index=True)
            st.success(f"Student {s_name} Added!")

            # Generate QR
            qr = qrcode.make(s_id)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf, caption=f"QR Code for {s_id}")
        else:
            st.error("Please fill all fields")

elif menu == "Mark Attendance":
    st.header("Mark Attendance")
    s_id = st.text_input("Enter Student ID / Scan QR")
    if st.button("Mark Present"):
        student = st.session_state.students[st.session_state.students["ID"] == s_id]
        if not student.empty:
            name = student.iloc[0]["Name"]
            now = datetime.datetime.now()
            new_att = pd.DataFrame([[s_id, name, now.date(), now.time(), "Present"]],
                                   columns=["ID", "Name", "Date", "Time", "Status"])
            st.session_state.attendance = pd.concat([st.session_state.attendance, new_att], ignore_index=True)
            st.success(f"Attendance Marked for {name}!")
        else:
            st.error("Student not found! Please Add Student first.")

elif menu == "View Records":
    st.header("All Records")
    st.subheader("Students List")
    st.dataframe(st.session_state.students)
    st.subheader("Attendance Records")
    st.dataframe(st.session_state.attendance)
    if not st.session_state.attendance.empty:
        csv = st.session_state.attendance.to_csv(index=False).encode('utf-8')
        st.download_button("Download Attendance CSV", csv, "attendance.csv", "text/csv")
