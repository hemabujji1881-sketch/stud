import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Student Details Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Details Analytics Dashboard")
st.markdown(
    "Interactive dashboard for analyzing student performance, "
    "attendance and academic details."
)

# ---------------------------------------------------
# SAMPLE STUDENT DATA
# ---------------------------------------------------

np.random.seed(42)

names = [
    "Hema", "Anjali", "Rahul", "Suresh", "Priya",
    "Kiran", "Sneha", "Arjun", "Divya", "Vijay",
    "Pooja", "Ravi", "Keerthi", "Manoj", "Swathi",
    "Harsha", "Nikhil", "Lavanya", "Sai", "Teja"
]

departments = ["CSE", "AIML", "ECE", "EEE"]
genders = ["Male", "Female"]
years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

data = []

for i in range(100):

    name = np.random.choice(names) + f" {i+1}"

    math = np.random.randint(45, 100)
    python = np.random.randint(45, 100)
    dbms = np.random.randint(45, 100)
    dsa = np.random.randint(45, 100)

    average = round(
        (math + python + dbms + dsa) / 4, 2
    )

    attendance = np.random.randint(60, 100)

    if average >= 90:
        grade = "A+"
    elif average >= 80:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"

    data.append({
        "Student ID": f"STU{i+1:03}",
        "Name": name,
        "Department": np.random.choice(departments),
        "Gender": np.random.choice(genders),
        "Year": np.random.choice(years),
        "Maths": math,
        "Python": python,
        "DBMS": dbms,
        "DSA": dsa,
        "Attendance": attendance,
        "Average Marks": average,
        "Grade": grade
    })

df = pd.DataFrame(data)

# ---------------------------------------------------
# CSV UPLOAD
# ---------------------------------------------------

st.sidebar.header("📂 Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload Student CSV",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        uploaded_df = pd.read_csv(uploaded_file)

        required_columns = [
            "Student ID",
            "Name",
            "Department",
            "Gender",
            "Year",
            "Maths",
            "Python",
            "DBMS",
            "DSA",
            "Attendance",
            "Average Marks",
            "Grade"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in uploaded_df.columns
        ]

        if missing_columns:

            st.error(
                "Missing columns: "
                + ", ".join(missing_columns)
            )

        else:
            df = uploaded_df.copy()
            st.success("CSV uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")


# ---------------------------------------------------
# SIDEBAR MULTI-SELECT FILTERS
# ---------------------------------------------------

st.sidebar.header("🔎 Student Filters")

selected_departments = st.sidebar.multiselect(
    "Select Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

selected_genders = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

selected_grades = st.sidebar.multiselect(
    "Select Grade",
    options=sorted(df["Grade"].unique()),
    default=sorted(df["Grade"].unique())
)


# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered_df = df[
    (df["Department"].isin(selected_departments)) &
    (df["Gender"].isin(selected_genders)) &
    (df["Year"].isin(selected_years)) &
    (df["Grade"].isin(selected_grades))
].copy()


# ---------------------------------------------------
# DASHBOARD KPI CARDS
# ---------------------------------------------------

st.subheader("📊 Student Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Students",
        len(filtered_df)
    )

with col2:
    avg_marks = (
        filtered_df["Average Marks"].mean()
        if len(filtered_df) > 0 else 0
    )

    st.metric(
        "Average Marks",
        f"{avg_marks:.2f}"
    )

with col3:
    avg_attendance = (
        filtered_df["Attendance"].mean()
        if len(filtered_df) > 0 else 0
    )

    st.metric(
        "Average Attendance",
        f"{avg_attendance:.2f}%"
    )

with col4:

    passed = (
        len(
            filtered_df[
                filtered_df["Average Marks"] >= 40
            ]
        )
        if len(filtered_df) > 0
        else 0
    )

    pass_percentage = (
        (passed / len(filtered_df)) * 100
        if len(filtered_df) > 0
        else 0
    )

    st.metric(
        "Pass Percentage",
        f"{pass_percentage:.1f}%"
    )


# ---------------------------------------------------
# NO DATA CHECK
# ---------------------------------------------------

if filtered_df.empty:

    st.warning(
        "No students match the selected filters."
    )

    st.stop()


# ---------------------------------------------------
# STUDENT DETAILS TABLE
# ---------------------------------------------------

st.subheader("👨‍🎓 Student Details")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------
# GRAPH 1 — STUDENTS BY DEPARTMENT
# ---------------------------------------------------

st.subheader("📚 Students by Department")

department_count = (
    filtered_df["Department"]
    .value_counts()
    .reset_index()
)

department_count.columns = [
    "Department",
    "Students"
]

fig_department = px.bar(
    department_count,
    x="Department",
    y="Students",
    text="Students",
    title="Number of Students by Department"
)

fig_department.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_department,
    use_container_width=True
)


# ---------------------------------------------------
# GRAPH 2 — GENDER DISTRIBUTION
# ---------------------------------------------------

st.subheader("👥 Gender Distribution")

gender_count = (
    filtered_df["Gender"]
    .value_counts()
    .reset_index()
)

gender_count.columns = [
    "Gender",
    "Students"
]

fig_gender = px.pie(
    gender_count,
    names="Gender",
    values="Students",
    hole=0.4,
    title="Gender Distribution"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ---------------------------------------------------
# GRAPH 3 — SUBJECT PERFORMANCE
# ---------------------------------------------------

st.subheader("📖 Average Subject Performance")

subject_columns = [
    "Maths",
    "Python",
    "DBMS",
    "DSA"
]

subject_average = (
    filtered_df[subject_columns]
    .mean()
    .reset_index()
)

subject_average.columns = [
    "Subject",
    "Average Marks"
]

fig_subject = px.bar(
    subject_average,
    x="Subject",
    y="Average Marks",
    text_auto=".2f",
    title="Average Marks by Subject"
)

st.plotly_chart(
    fig_subject,
    use_container_width=True
)


# ---------------------------------------------------
# GRAPH 4 — ATTENDANCE VS MARKS
# ---------------------------------------------------

st.subheader("📈 Attendance vs Average Marks")

fig_scatter = px.scatter(
    filtered_df,
    x="Attendance",
    y="Average Marks",
    color="Department",
    hover_data=[
        "Name",
        "Student ID",
        "Year",
        "Grade"
    ],
    title="Attendance vs Student Performance"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ---------------------------------------------------
# GRAPH 5 — PERFORMANCE BY YEAR
# ---------------------------------------------------

st.subheader("🎓 Performance by Academic Year")

year_average = (
    filtered_df
    .groupby("Year")["Average Marks"]
    .mean()
    .reset_index()
)

fig_year = px.line(
    year_average,
    x="Year",
    y="Average Marks",
    markers=True,
    title="Average Performance by Academic Year"
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# ---------------------------------------------------
# GRAPH 6 — GRADE DISTRIBUTION
# ---------------------------------------------------

st.subheader("🏆 Grade Distribution")

grade_count = (
    filtered_df["Grade"]
    .value_counts()
    .reset_index()
)

grade_count.columns = [
    "Grade",
    "Students"
]

fig_grade = px.bar(
    grade_count,
    x="Grade",
    y="Students",
    text="Students",
    title="Number of Students by Grade"
)

st.plotly_chart(
    fig_grade,
    use_container_width=True
)


# ---------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------

st.subheader("⬇️ Download Data")

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Student Data",
    data=csv_data,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Dynamic Student Data Visualization Dashboard | "
    "Python + Streamlit + Pandas + Plotly"
)