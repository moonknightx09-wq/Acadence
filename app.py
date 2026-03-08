import streamlit as st
import json
import os
import subprocess
from ai_model import generate_quiz, ask_tutor

# ---------- DATABASE FUNCTIONS ----------

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

def save_users(users_dict):
    with open("users.json", "w") as file:
        json.dump(users_dict, file, indent=4)

st.set_page_config(page_title="Acadence", page_icon="🎓", layout="wide")

def load_performance():
    if os.path.exists("performance.json"):
        with open("performance.json", "r") as file:
            return json.load(file)
    return {}

def save_performance(data):
    with open("performance.json", "w") as file:
        json.dump(data, file, indent=4)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "Login"

if "users" not in st.session_state:
    st.session_state.users = load_users()

if "performance" not in st.session_state:
    st.session_state.performance = load_performance()

# ---------- IF NOT LOGGED IN ----------
if not st.session_state.logged_in:

    st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Sidebar hidden clean look */
section[data-testid="stSidebar"] {
    background: #0f172a;
}

/* Main container card effect */
.block-container {
    background-color: rgba(30, 41, 59, 0.85);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

/* Titles */
h1, h2, h3 {
    color: #22D3EE;
}

/* Input fields */
input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid #334155 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #06b6d4, #0ea5e9);
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0891b2, #0284c7);
}

</style>
""", unsafe_allow_html=True)

    # Center layout using columns
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<h1 style='text-align:center;'>Acadence </h1>", unsafe_allow_html=True)

        # -------- LOGIN PAGE --------
        if st.session_state.page == "Login":

            st.subheader("Login")

           
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):

                if username in st.session_state.users:

                    stored_user = st.session_state.users[username]

                    if password == stored_user["password"]:

                        st.session_state.logged_in = True
                        st.session_state.role = stored_user["role"]
                        st.session_state.username = username
                        st.session_state.name = stored_user["name"]

                        st.rerun()

                    else:
                        st.error("Incorrect password")

                else:
                    st.error("User not found")

            if st.button("Go to Sign Up"):
                st.session_state.page = "Sign Up"
                st.rerun()
                    
        # -------- SIGN UP PAGE --------
        elif st.session_state.page == "Sign Up":

            st.subheader("Create Account")

            full_name = st.text_input("Full Name")
            username = st.text_input("Choose Username")
            new_role = st.selectbox("Select Role", ["Student", "Teacher", "Parent"])
            child_username = None
            if new_role == "Parent":
                child_username = st.text_input("Enter Child Username")

            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Re-enter Password", type="password")

            if st.button("Create Account"):

                if not full_name or not username or not new_password or not confirm_password:
                    st.error("Please fill all fields")

                elif new_password != confirm_password:
                    st.error("Passwords do not match")

                elif username in st.session_state.users:
                    st.error("Username already exists")

                elif new_role == "Parent" and child_username not in st.session_state.users:
                    st.error("Child username does not exist")

                else:
                    user_data = {
                        "name": full_name,
                        "password": new_password,
                        "role": new_role
                    }

                    if new_role == "Parent":
                        user_data["child"] = child_username

                    st.session_state.users[username] = user_data
                    save_users(st.session_state.users)

                    st.success("Account created successfully")

            if st.button("Back to Login"):
                st.session_state.page = "Login"
                st.rerun()

# ---------- DASHBOARDS ----------
else:

    st.sidebar.write(f"Logged in as: {st.session_state.role}")

    if st.sidebar.button("Logout"):

        # Clear entire session safely
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()

    # ================= STUDENT =================
    if st.session_state.role == "Student":

        st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

section[data-testid="stSidebar"] {
    background: #111827;
}

h1, h2, h3 {
    color: #10B981;
}

.stButton > button {
    background: #10B981;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton > button:hover {
    background: #059669;
}

[data-testid="stMetricValue"] {
    color: #34D399;
}
</style>
""", unsafe_allow_html=True)

        clean_name = st.session_state.name

        st.markdown("# Student Dashboard")
        st.markdown("---")

        # TOP
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"## Welcome, {clean_name}")
            st.write("Ready to continue learning?")

        with col2:
            st.markdown("### Academic Summary")
            st.markdown(
                """
                <div style="
                    background-color:#1f3b5c;
                    padding:15px;
                    border-radius:10px;
                    color:white;
                ">
                Marks will appear here.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # PROGRESS
        st.markdown("### Progress Overview")

        username = st.session_state.username
        performance = st.session_state.performance

        if username in performance and performance[username]["scores"]:

            scores = performance[username]["scores"]
            avg_score = round(sum(scores) / len(scores), 2)

            col1, col2 = st.columns(2)
            col1.metric("Total Assessments", len(scores))
            col2.metric("Average Performance", f"{avg_score}%")

            st.line_chart({"Performance": scores})

            if len(scores) >= 2:
                trend = scores[-1] - scores[-2]
                predicted = max(0, min(100, scores[-1] + trend))
                st.info(f"AI Predicted Next Score: {round(predicted,2)}%")

        else:
            st.info("No assessment data available yet.")

        # LEARNING TOOLS (INSIDE STUDENT BLOCK)
        st.markdown("## Learning Tools")

        if "student_tab" not in st.session_state:
            st.session_state.student_tab = "home"

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Take Quiz"):
                st.session_state.student_tab = "quiz"

        with col2:
            if st.button("AI Tutor"):
                st.session_state.student_tab = "ai"

        st.markdown("---")

        if st.session_state.student_tab == "home":
            st.write("Select a tool to begin.")

        elif st.session_state.student_tab == "quiz":

            st.markdown("## Quiz Portal")

            tab1, tab2 = st.tabs([" Teacher Assigned Quiz", " Practice Quiz"])

            # ==========================================================
            # TAB 1 → TEACHER ASSIGNED QUIZ
            # ==========================================================
            with tab1:

                if os.path.exists("assigned_quizzes.json"):
                    with open("assigned_quizzes.json", "r") as f:
                        assigned_data = json.load(f)
                else:
                    assigned_data = {"quizzes": []}

                class_quizzes = assigned_data.get("quizzes", [])

                if not class_quizzes:
                    st.info("No quiz assigned by teacher yet.")
                else:
                    latest_quiz = class_quizzes[-1]
                    quiz = latest_quiz["questions"]

                    st.markdown(f"### {latest_quiz['subject']} — {latest_quiz['topic']}")
                    st.caption(f"Assigned by {latest_quiz['created_by']}")

                    for i, q in enumerate(quiz):
                        st.write(f"Q{i+1}. {q['question']}")
                        st.radio("Choose answer", q["options"], key=f"assigned_{i}", index=None)
                        st.write("---")

                    if st.button("Submit Assigned Quiz"):

                        score = 0
                        wrong_topics = []

                        for i, q in enumerate(quiz):

                            selected = st.session_state.get(f"assigned_{i}")
                            question_text = q["question"]

                            st.write(f"Q{i+1}. {question_text}")

                            if selected is None:
                                st.warning("Not attempted")
                                wrong_topics.append(question_text)

                            elif selected == q["correct_answer"]:
                                st.success("Correct")
                                score += 1

                            else:
                                st.error(f"Wrong | Correct answer: {q['correct_answer']}")
                                wrong_topics.append(question_text)

                            if "explanation" in q:
                                st.info(f"Explanation: {q['explanation']}")

                            st.write("---")

                        percentage = round((score / len(quiz)) * 100, 2)

                        # Blockchain hash
                        result = subprocess.run(
                            ["node", "test_weil.js", st.session_state.username, str(percentage)],
                            capture_output=True,
                            text=True
                        )

                        blockchain_hash = result.stdout.strip()

                        st.success("Academic record secured on WeilChain")
                        st.write("Blockchain Hash:", blockchain_hash)

                        # Save in teacher.json
                        if os.path.exists("teacher.json"):
                            with open("teacher.json", "r") as f:
                                teacher_data = json.load(f)
                        else:
                            teacher_data = {"records": []}

                        teacher_data["records"].append({
                            "teacher_id": latest_quiz["created_by"],
                            "subject": latest_quiz["subject"],
                            "topic": latest_quiz["topic"],
                            "student_name": st.session_state.name,
                            "score": percentage,
                            "weak_topics": wrong_topics,
                            "blockchain_hash": blockchain_hash
                        })

                        with open("teacher.json", "w") as f:
                            json.dump(teacher_data, f, indent=4)

                        st.success(f"Final Score: {score}/{len(quiz)} ({percentage}%)")

            # ==========================================================
            # TAB 2 → PRACTICE QUIZ (YOUR ORIGINAL LOGIC)
            # ==========================================================
            with tab2:

                topic = st.text_input("Enter topic for quiz")

                if st.button("Generate Quiz"):
                    st.session_state.pop("weak_topics", None)

                    with st.spinner("Generating quiz..."):
                        quiz = generate_quiz(topic)

                    st.session_state.current_quiz = quiz

                if "current_quiz" in st.session_state:

                    for i, q in enumerate(st.session_state.current_quiz):
                        st.write(f"Q{i+1}. {q['question']}")
                        selected = st.radio(
                            "Choose answer:",
                            q["options"],
                            key=f"q_{i}",
                            index=None
                        )
                        st.write("---")

                    if st.button("Submit Quiz"):

                        score = 0
                        wrong_topics = []

                        for i, q in enumerate(st.session_state.current_quiz):

                            selected = st.session_state.get(f"q_{i}")
                            question_text = q["question"]

                            st.write(f"Q{i+1}. {question_text}")

                            if selected is None:
                                st.warning("Not attempted")
                                wrong_topics.append(question_text)

                            elif selected == q["correct_answer"]:
                                st.success("Correct")
                                score += 1

                            else:
                                st.error(f"Wrong | Correct answer: {q['correct_answer']}")
                                wrong_topics.append(question_text)

                            if "explanation" in q:
                                st.info(f"Explanation: {q['explanation']}")

                            st.write("---")

                        username = st.session_state.username

                        if username not in st.session_state.performance:
                            st.session_state.performance[username] = {
                                "scores": [],
                                "weak_topics": []
                            }

                        percentage = round((score / len(st.session_state.current_quiz)) * 100, 2)

                        result = subprocess.run(
                            ["node", "test_weil.js", username, str(percentage)],
                            capture_output=True,
                            text=True
                        )

                        blockchain_hash = result.stdout.strip()

                        st.success("Academic record secured on WeilChain")
                        st.write("Blockchain Hash:", blockchain_hash)

                        st.session_state.performance[username]["scores"].append({
                            "subject": latest_quiz["subject"],
                            "topic": latest_quiz["topic"],
                            "score": percentage
                        })
                        st.session_state.performance[username]["weak_topics"] = wrong_topics

                        save_performance(st.session_state.performance)

                        st.success(f"Final Score: {score}/{len(st.session_state.current_quiz)} ({percentage}%)")

        elif st.session_state.student_tab == "ai":

            username = st.session_state.username
            performance = st.session_state.performance

            if username in performance and performance[username]["weak_topics"]:

                st.subheader("Your Weak Areas")

                weak_list = performance[username]["weak_topics"]

                for i, topic in enumerate(weak_list):
                    if st.button(f"Explain: {topic}", key=f"weak_{i}"):

                        with st.spinner("Generating solution..."):
                            explanation = ask_tutor(topic)

                        st.write(explanation)

            else:
                st.info("No weak areas detected yet.")

            st.markdown("---")

            st.subheader("Ask AI Tutor")
            question = st.text_input("Ask your doubt")

            if st.button("Ask Tutor"):
                with st.spinner("Thinking..."):
                    answer = ask_tutor(question)
                st.write(answer)

    # ================= TEACHER =================
    elif st.session_state.role == "Teacher":

        st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e1e2f, #2a2a4a);
}

section[data-testid="stSidebar"] {
    background: #111827;
}

h1, h2, h3 {
    color: #8B5CF6;
}

.stButton > button {
    background: #8B5CF6;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton > button:hover {
    background: #7C3AED;
}

[data-testid="stMetricValue"] {
    color: #A78BFA;
}
</style>
""", unsafe_allow_html=True)

        st.title("Teacher Dashboard")
        st.markdown(f"### Welcome, {st.session_state.name}")
        st.markdown("---")

        # ================= LOAD DATA =================
        if os.path.exists("teacher.json"):
            with open("teacher.json", "r") as f:
                teacher_data = json.load(f)
        else:
            teacher_data = {"records": []}

        if os.path.exists("assigned_quizzes.json"):
            with open("assigned_quizzes.json", "r") as f:
                assigned_data = json.load(f)
        else:
            assigned_data = {"quizzes": []}

        records = teacher_data.get("records", [])

        # ================= CREATE QUIZ =================
        st.subheader("Assign Quiz To Class")

        subject_input = st.text_input("Enter Subject")
        topic_input = st.text_input("Enter Topic")

        if st.button("Generate & Assign Quiz"):

            if not subject_input or not topic_input:
                st.warning("Please fill subject and topic.")
            else:
                with st.spinner("Generating quiz..."):
                    quiz = generate_quiz(subject_input, topic_input)

                assigned_data["quizzes"].append({
                    "quiz_id": str(len(assigned_data["quizzes"]) + 1),
                    "subject": subject_input,
                    "topic": topic_input,
                    "questions": quiz,
                    "created_by": st.session_state.name
                })

                with open("assigned_quizzes.json", "w") as f:
                    json.dump(assigned_data, f, indent=4)

                st.success("Quiz Assigned Successfully!")

        st.markdown("---")

        # ================= ANALYTICS =================
        st.subheader("Class Performance Overview")

        if not records:
            st.info("No quiz submissions yet.")
            st.stop()

        avg_score = sum(r["score"] for r in records) / len(records)

        st.metric("Total Submissions", len(records))
        st.metric("Average Score", f"{round(avg_score,2)}%")

        st.progress(int(avg_score))

        st.markdown("---")

        # ================= STUDENT CATEGORIES =================
        best, good, average, below = [], [], [], []
        weak_counter = {}

        for r in records:
            name = r["student_name"]
            score = r["score"]

            if score >= 80:
                best.append(name)
            elif score >= 60:
                good.append(name)
            elif score >= 40:
                average.append(name)
            else:
                below.append(name)

            for wt in r.get("weak_topics", []):
                weak_counter[wt] = weak_counter.get(wt, 0) + 1

        col1, col2, col3, col4 = st.columns(4)

        def colored_card(column, title, students, bg_color):

            with column:

                if students:
                    student_html = ""
                    for s in students:
                        student_html += f"<p style='margin:6px 0;'>• {s}</p>"
                else:
                    student_html = "<p style='opacity:0.7;'>No Students</p>"

                st.markdown(f"""
                <div style="
                    background:{bg_color};
                    border-radius:16px;
                    padding:20px;
                    min-height:220px;
                    box-shadow:0 10px 20px rgba(0,0,0,0.4);
                    color:white;
                ">
                    <h3 style="margin-bottom:15px;">{title}</h3>
                    {student_html}
                </div>
                """, unsafe_allow_html=True)

        colored_card(col1, "Best", list(set(best)), "#15803d")       # Green
        colored_card(col2, "Good", list(set(good)), "#ea580c")       # Orange
        colored_card(col3, "Average", list(set(average)), "#ca8a04") # Yellow
        colored_card(col4, "Below", list(set(below)), "#b91c1c")     # Red

        st.markdown("---")

        # ================= WEAK TOPICS =================
        st.subheader("Common Weak Topics")

        if weak_counter:
            sorted_topics = sorted(weak_counter.items(), key=lambda x: x[1], reverse=True)
            for topic, count in sorted_topics:
                st.write(f"{topic} — {count} students struggled")
        else:
            st.write("No weak topics yet.")

        st.markdown("---")

        # ================= BLOCKCHAIN RECORDS =================
        st.subheader("Verified Academic Records")

        for r in records:
            st.markdown(f"""
            ---
            **Subject:** {r.get('subject', 'N/A')}  
            **Topic:** {r.get('topic', 'N/A')}  
            **Score:** {r.get('score', 'N/A')}%  
            **Blockchain Hash:** `{r.get('blockchain_hash', 'Not Available')}`
                        """)

    # ================= PARENT =================
    elif st.session_state.role == "Parent":

        st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f2937, #111827);
}

section[data-testid="stSidebar"] {
    background: #0f172a;
}

h1, h2, h3 {
    color: #F59E0B;
}

.stButton > button {
    background: #F59E0B;
    color: black;
    border-radius: 8px;
    border: none;
}

.stButton > button:hover {
    background: #D97706;
}

[data-testid="stMetricValue"] {
    color: #FBBF24;
}
</style>
""", unsafe_allow_html=True)

        parent_user = st.session_state.username
        parent_name = st.session_state.name
        child = st.session_state.users[parent_user].get("child")

        # Smart Header
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #1f2937, #111827);
            padding: 25px;
            border-radius: 18px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        ">
            <h2 style="margin:0; color:#F59E0B;">
                  Parent Dashboard
            </h2>
            <p style="margin-top:8px; font-size:18px;">
                <strong>Parent:</strong> {parent_name} <br>
                <strong>Monitoring Student:</strong> {child}
            </p>
        </div>
        """, unsafe_allow_html=True)
        parent_user = st.session_state.username
        child = st.session_state.users[parent_user].get("child")

        if not child:
            st.warning("No child linked.")
            st.stop()

        performance = st.session_state.performance

        if child in performance and performance[child]["scores"]:

            scores = performance[child]["scores"]

            avg_score = round(sum(scores) / len(scores), 2)

            col1, col2 = st.columns(2)
            col1.metric("Total Assessments", len(scores))
            col2.metric("Average Performance", f"{avg_score}%")

            st.line_chart({"Performance": scores})

        else:

            st.info("No performance data available yet.")