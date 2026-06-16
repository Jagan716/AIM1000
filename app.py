import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database Connection
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

st.title("🚀 AIM1000")

title = st.text_input("Task Title")

description = st.text_area("Task Description")

category = st.selectbox(
    "Category",
    ["Learning", "Career", "Development", "Personal"]
)

priority = st.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
)

status = st.selectbox(
    "Status",
    ["Pending", "In Progress", "Completed"]
)

if st.button("Save Task"):

    cursor.execute(
        """
        INSERT INTO tasks
        (title, description, category, priority, status)

        VALUES (?, ?, ?, ?, ?)
        """,
       (
        title,
        description,
        category,
        priority,
        status
        )
    )

    conn.commit()

    st.success("Task Saved Successfully!")

# Display Tasks
st.subheader("📋 Saved Tasks")
st.subheader("📊 Tasks by Category")

df = pd.read_sql_query(
    "SELECT * FROM tasks",
    conn
)

if not df.empty:

    category_counts = df["category"].value_counts()

    fig, ax = plt.subplots()

    category_counts.plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)



df.to_csv("tasks.csv", index=False)

with open("tasks.csv", "rb") as file:

    st.download_button(
        "📥 Download Tasks",
        file,
        "tasks.csv"
    )


st.subheader("🗑️ Delete Task")

delete_id = st.number_input(
    "Enter Task ID",
    min_value=1,
    step=1
)

if st.button("Delete Task"):

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (delete_id,)
    )

    conn.commit()

    st.success("Task Deleted Successfully!")

st.subheader("✏️ Update Task Status")

update_id = st.number_input(
    "Task ID to Update",
    min_value=1,
    step=1,
    key="update_id"
)

new_status = st.selectbox(
    "New Status",
    ["Pending", "In Progress", "Completed"]
)

if st.button("Update Status"):

    cursor.execute(
        """
        UPDATE tasks
        SET status=?
        WHERE id=?
        """,
        (new_status, update_id)
    )

    conn.commit()

    st.success("Status Updated Successfully!")

cursor.execute("SELECT * FROM tasks")

tasks = cursor.fetchall()



total_tasks = len(tasks)

pending_tasks = 0
completed_tasks = 0

for task in tasks:

    if task[5] == "Pending":
        pending_tasks += 1

    if task[5] == "Completed":
        completed_tasks += 1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tasks", total_tasks)

with col2:
    st.metric("Pending", pending_tasks)

with col3:
    st.metric("Completed", completed_tasks)

score = 0

if total_tasks > 0:
    score = (completed_tasks / total_tasks) * 100

st.metric(
    "⭐ Productivity Score",
    f"{score:.0f}%"
)

search = st.text_input("🔍 Search Task")


for task in tasks:

    if search.lower() in task[1].lower():

        st.write(
            f"ID: {task[0]} | Title: {task[1]} | Category: {task[3]} | Priority: {task[4]} | Status: {task[5]}"
        )