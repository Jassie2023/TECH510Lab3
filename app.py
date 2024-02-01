import streamlit as st
import sqlite3

# Database connection
DB_PATH = "todoapp.sqlite"
con = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = con.cursor()

def toggle_is_done(task_id, is_done):
    cur.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (is_done, task_id))
    con.commit()

def delete_task(task_id):
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()

def main():
    st.title("Todo App")

    # Task creation form
    with st.form("task_form"):
        name = st.text_input("Task Name")
        description = st.text_area("Task Description")
        submit_button = st.form_submit_button("Submit")
        if submit_button and name:
            cur.execute("INSERT INTO tasks (name, description, is_done) VALUES (?, ?, ?)", 
                        (name, description, False))
            con.commit()

    # Search and filter
    search_query = st.text_input("Search Tasks")
    status_filter = st.selectbox("Filter by status", ["All", "Done", "Not Done"])

    query = "SELECT * FROM tasks WHERE name LIKE ?"
    if status_filter == "Done":
        query += " AND is_done = 1"
    elif status_filter == "Not Done":
        query += " AND is_done = 0"
    tasks = cur.execute(query, ('%' + search_query + '%',)).fetchall()

    for task in tasks:
        cols = st.columns([3, 1, 1])
        id, name, description, is_done = task
        with cols[0]:
            st.text(f"Name: {name}\nDescription: {description}")
        with cols[1]:
            if st.button("Done", key=f"done-{id}"):
                toggle_is_done(id, not is_done)
        with cols[2]:
            if st.button("Delete", key=f"delete-{id}"):
                delete_task(id)

if __name__ == "__main__":
    main()

