import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Attendance & Performance Analyzer",
    page_icon="🎓",
    layout="wide",
)

# Dark Theme & Custom Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .card {
        background-color: #1e2129;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d3139;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "user_type" not in st.session_state:
  st.session_state.user_type = None
if "username" not in st.session_state:
  st.session_state.username = None
if "user_data" not in st.session_state:
  st.session_state.user_data = None

# ----------------- LOGIN SCREEN -----------------
if not st.session_state.logged_in:
  st.markdown(
      "<h1 style='text-align: center; color: #FF416C;'>🎓 Smart Attendance &"
      " Performance Analyzer</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='text-align: center; color: #a1a1a1;'>Student & Faculty Login"
      " Portal (JNTUK R23)</h4>",
      unsafe_allow_html=True,
  )
  st.write("")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    tab1, tab2 = st.tabs(["👨‍🎓 Student Login", "👨‍🏫 Faculty Login"])

    with tab1:
      s_roll = st.text_input("Enter Roll Number", key="s_roll")
      s_pass = st.text_input("Enter Password", type="password", key="s_pass")

      if st.button("Login as Student"):
        if os.path.exists("students.csv"):
          df = pd.read_csv("students.csv")
          df.columns = df.columns.str.strip()
          df["Roll_Number"] = df["Roll_Number"].astype(str).str.strip()
          df["Password"] = df["Password"].astype(str).str.strip()

          match = df[
              (df["Roll_Number"] == s_roll.strip())
              & (df["Password"] == s_pass.strip())
          ]
          if not match.empty:
            st.session_state.logged_in = True
            st.session_state.user_type = "student"
            st.session_state.username = match.iloc[0]["Name"]
            st.session_state.user_data = match.iloc[0].to_dict()
            st.success(f"Welcome, {st.session_state.username}!")
            st.rerun()
          else:
            st.error("Invalid Roll Number or Password!")
        else:
          st.error("students.csv file not found!")

    with tab2:
      f_user = st.text_input("Admin Username", key="f_user")
      f_pass = st.text_input("Admin Password", type="password", key="f_pass")

      if st.button("Login as Faculty"):
        if f_user == "admin" and f_pass == "admin123":
          st.session_state.logged_in = True
          st.session_state.user_type = "faculty"
          st.session_state.username = "Faculty Administrator"
          st.success("Faculty Login Successful!")
          st.rerun()
        else:
          st.error("Invalid Credentials! (Use admin / admin123)")

# ----------------- MAIN APP & MODULES (AFTER LOGIN) -----------------
else:
  st.sidebar.title(f"👤 {st.session_state.username}")
  st.sidebar.info(f"Role: {st.session_state.user_type.capitalize()}")

  if st.sidebar.button("🚪 Logout System"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.session_state.user_data = None
    st.rerun()

  # Student View
  if st.session_state.user_type == "student":
    st.title(
        f"🌟 Welcome, {st.session_state.username} (Student Portal)"
    )
    st.markdown("---")

    menu = st.sidebar.radio(
        "Navigation Menu",
        [
            "🏠 Dashboard",
            "📊 Attendance Tracker",
            "📝 Assignment Tracker",
            "📚 Study Planner",
            "📈 Performance Analysis",
            "🤖 AI Suggestions",
            "📊 Reports & Graphs",
            "🎓 Curriculum & Results",
        ],
    )

    u_data = st.session_state.user_data
    att_val = float(u_data.get("Attendance", 80))
    cgpa_val = float(u_data.get("CGPA", 8.5))

    if menu == "🏠 Dashboard":
      st.subheader("📌 Student Dashboard & Summary")
      c1, c2, c3 = st.columns(3)
      c1.metric("Attendance", f"{att_val}%")
      c2.metric("CGPA", f"{cgpa_val} / 10")
      c3.metric("Section", u_data.get("Section", "D1"))

      st.markdown("""
                <div class="card">
                    <h3>💡 Quick Portal Overview</h3>
                    <p>Use the left sidebar navigation menu to view your detailed Attendance, Assignments, Study Planner, Performance Analysis, JNTUK R23 Curriculum, and AI Recommendations.</p>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "📊 Attendance Tracker":
      st.subheader("📊 Attendance Tracker")
      st.write(
          f"**Roll Number:** {u_data.get('Roll_Number')} | **Name:**"
          f" {u_data.get('Name')}"
      )
      st.progress(int(min(att_val, 100)))
      st.write(f"**Your Attendance Percentage:** {att_val}%")

      if att_val < 75:
        st.error(
            "⚠️ **Warning:** Your attendance is below 75%! Please maintain regular"
            " attendance."
        )
      else:
        st.success(
            "✅ Excellent! Your attendance is safe (above 75% criteria)."
        )

    elif menu == "📝 Assignment Tracker":
      st.subheader("📝 Assignment Tracker & Status")
      st.info("📌 **Pending Assignments:**")
      st.write("- Advanced Data Structures Lab Record (Due: Aug 05)")
      st.write("- Java Mini Project Report (Due: Aug 10)")
      st.success("✅ **Submitted Assignments:**")
      st.write("- DBMS Normalization Homework (Status: Submitted & Checked)")

    elif menu == "📚 Study Planner":
      st.subheader("📚 Daily Study Schedule & Timings")
      st.info("🌅 **Morning Session (9:00 AM - 12:00 PM):** Core Subjects")
      st.info("☀️ **Afternoon Session (1:00 PM - 4:00 PM):** Labs & Coding")
      st.info(
          "🌙 **Evening Session (6:00 PM - 8:00 PM):** Revision & Assignments"
      )

    elif menu == "📈 Performance Analysis":
      st.subheader("📈 Performance Analysis & CGPA")
      st.metric(label="Current Predicted CGPA", value=f"{cgpa_val} / 10")

      subjects = ["ADS", "DMGT", "AI", "Java", "UHV"]
      marks = [85, 92, 78, 88, 90]
      chart_data = pd.DataFrame({"Marks": marks}, index=subjects)
      st.bar_chart(chart_data)

    elif menu == "🤖 AI Suggestions":
      st.subheader("🤖 AI-Powered Personalized Suggestions")
      if att_val < 75:
        st.warning(
            "💡 **AI Tip:** Your attendance is low. Focus on attending upcoming"
            " classes consistently."
        )
      else:
        st.success(
            "💡 **AI Tip:** Great attendance record! Keep up the consistency in"
            " your academics."
        )
      st.info(
          "💡 **Study Recommendation:** Dedicate 1 extra hour to ADS and AI to"
          " improve overall semester grades."
      )

    elif menu == "📊 Reports & Graphs":
      st.subheader("📊 Reports & Downloads")
      report_df = pd.DataFrame({
          "Subject": ["ADS", "DMGT", "AI", "Java"],
          "Attendance": [f"{att_val}%", "90%", "75%", "85%"],
          "Marks": [85, 92, 78, 88],
      })
      st.dataframe(report_df, use_container_width=True)

      csv_data = report_df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Download Attendance & Marks Report (CSV)",
          data=csv_data,
          file_name=f"{u_data.get('Name')}_Report.csv",
          mime="text/csv",
      )

    elif menu == "🎓 Curriculum & Results":
      st.subheader("🎓 JNTUK R23 Curriculum & Status")
      st.info(
          "ℹ️ **Current Status:** 1st Sem Results Released | 2nd Sem Results"
          " Awaiting | 3rd Sem Started"
      )

      tab_s1, tab_s2, tab_s3 = st.tabs([
          "1st Year - 1st Sem (Results)",
          "1st Year - 2nd Sem",
          "2nd Year - 3rd Sem (Current)",
      ])

      with tab_s1:
        st.write("### 1st Semester Subjects & Status")
        st.success("📊 Results Status: Released")
        st.markdown("""
                * **Physics** - Status: Completed / Passed
                * **M1 (Mathematics-I)** - Status: Completed / Passed
                * **BEEE (Basic Electrical & Electronics Engineering)** - Status: Completed / Passed
                * **C Language (Programming for Problem Solving)** - Status: Completed / Passed
                * **Engineering Drawing** - Status: Completed / Passed
                """)

      with tab_s2:
        st.write("### 2nd Semester Subjects & Status")
        st.warning("⏳ Results Status: Awaiting / Yet to be Released")
        st.markdown("""
                * **Chemistry**
                * **Data Structures**
                * **M2 (Mathematics-II)**
                * **BCME (Basic Civil & Mechanical Engineering)**
                * **English**
                """)

      with tab_s3:
        st.write("### 2nd Year - 3rd Semester Subjects (Currently Ongoing)")
        st.success("🚀 Status: Classes Started")
        st.markdown("""
                * **ADS – Advanced Data Structures**
                * **DMGT – Discrete Mathematics and Graph Theory**
                * **Artificial Intelligence**
                * **Object Oriented Programming through Java**
                * **Universal Human Values – Understanding Harmony and Ethical Human Conduct**
                """)

  # Faculty View
  else:
    st.title("👨‍🏫 Faculty Administrator Control Panel")
    st.markdown("---")

    if os.path.exists("students.csv"):
      df_all = pd.read_csv("students.csv")
      df_all.columns = df_all.columns.str.strip()
      df_all["Attendance"] = pd.to_numeric(
          df_all["Attendance"], errors="coerce"
      )
      df_all["CGPA"] = pd.to_numeric(df_all["CGPA"], errors="coerce")

      c1, c2, c3 = st.columns(3)
      c1.metric("Total Students", len(df_all))
      c2.metric("Low Attendance (<75%)", len(df_all[df_all["Attendance"] < 75]))
      c3.metric("Top Performers", len(df_all[df_all["CGPA"] >= 9.0]))

      st.subheader("🔍 Search Student Records")
      search_q = st.text_input("Enter Roll Number or Name")
      if search_q:
        filtered = df_all[
            df_all["Roll_Number"].astype(str).str.contains(search_q)
            | df_all["Name"].str.contains(search_q, case=False)
        ]
        st.dataframe(filtered, use_container_width=True)
      else:
        st.subheader("📋 Complete Class List")
        st.dataframe(df_all, use_container_width=True)
    else:
      st.error("students.csv not found!")