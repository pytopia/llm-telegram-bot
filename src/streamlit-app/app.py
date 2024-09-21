import os

import streamlit as st
from dotenv import load_dotenv

from src.db import UserDatabase

# Load environment variables
load_dotenv()

# Get admin credentials from .env file
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Set page config
st.set_page_config(page_title="Telegram Bot User Management", page_icon="🤖")


def check_password():
    """Checks if the entered password is correct."""
    if "password_correct" not in st.session_state:
        with st.container():
            st.markdown("### 🔐 Admin Login")
            col1, col2 = st.columns(2)
            username = col1.text_input("👤 Username", key="username")
            password = col2.text_input("🔑 Password", type="password", key="password")
            if st.button("🚀 Login", use_container_width=True):
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state["password_correct"] = True
                    del st.session_state["password"]  # Don't store password
                    st.rerun()
                st.error("😕 User not known or password incorrect")
    return st.session_state.get("password_correct", False)


def add_user_form(db):
    """Renders and processes the add user form."""
    st.header("➕ Add New User")
    with st.form("add_user_form"):
        col1, col2, col3 = st.columns(3)
        new_username = col1.text_input("👤 Username")
        new_rate_limit = col2.number_input("⏱️ Rate Limit", min_value=1, value=100)
        is_authorized = col3.checkbox("✅ Is Authorized", value=True)

        if st.form_submit_button("➕ Add User", use_container_width=True):
            with db:
                db.add_user(new_username, is_authorized, new_rate_limit)
            st.success(f"✅ User {new_username} added successfully!")


def display_users(db):
    """Displays all users in a table."""
    st.header("👥 All Users")
    with db:
        users = db.get_all_users()

    if users:
        user_data = [{"👤 Username": u, "✅ Authorized": "Yes" if a else "No", "⏱️ Rate Limit": r} for u, a, r in users]
        st.table(user_data)
    else:
        st.info("📭 No users found in the database.")

    return users


def update_user_form(db, users):
    """Renders and processes the update user form."""
    st.header("🔄 Update User")
    with st.form("update_user_form"):
        col1, col2, col3 = st.columns(3)
        username = col1.selectbox("👤 Select User", [user[0] for user in users])
        rate_limit = col2.number_input("⏱️ New Rate Limit", min_value=1, value=100)
        is_authorized = col3.checkbox("✅ Is Authorized", value=True)

        col1, col2 = st.columns(2)
        update_button = col1.form_submit_button("🔄 Update User", use_container_width=True)
        delete_button = col2.form_submit_button("🗑️ Delete User", use_container_width=True)

        if update_button:
            with db:
                db.add_user(username, is_authorized, rate_limit)
            st.success(f"✅ User {username} updated successfully!")
            st.rerun()

        if delete_button:
            with db:
                db.delete_user(username)
            st.success(f"🗑️ User {username} deleted successfully!")
            st.rerun()


def main():
    st.title("🤖 Telegram Bot User Management")

    db = UserDatabase()

    add_user_form(db)
    users = display_users(db)
    update_user_form(db, users)


if __name__ == "__main__":
    if check_password():
        main()
    else:
        st.stop()
