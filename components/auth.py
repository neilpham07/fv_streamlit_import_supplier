import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

_USERS = {
    os.getenv("APP_USERNAME", "admin"): os.getenv("APP_PASSWORD", "admin123"),
    "j.doe@enterprise.com": "Admin@123",
}


def login_page():
    st.markdown("""
    <style>
    .block-container { padding-top: 4vh !important; }
    body { background: #f1f5f9; }
    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        # Logo
        st.image("image/logo finviet.png", width=160)

        st.markdown("""
        <p style="color:#64748b; margin:4px 0 24px; font-size:0.9rem;">
            Enterprise Master Data Management
        </p>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div class="field-label">Username or Business Email</div>', unsafe_allow_html=True)
            username = st.text_input(
                "username", placeholder="j.doe@enterprise.com",
                label_visibility="collapsed",
            )

            col_pw_label, col_fp = st.columns([2, 1])
            col_pw_label.markdown('<div class="field-label" style="margin-top:12px;">Password</div>', unsafe_allow_html=True)
            col_fp.markdown('<div style="text-align:right;margin-top:16px;font-size:0.78rem;color:#2563eb;cursor:pointer;">Forgot Password?</div>', unsafe_allow_html=True)

            password = st.text_input(
                "password", type="password",
                label_visibility="collapsed",
            )
            remember = st.checkbox("Remember this device for 30 days")  # noqa: F841

            submitted = st.form_submit_button(
                "SIGN IN →",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            if username in _USERS and _USERS[username] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.page = "supplier_manage"
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

        st.markdown("""
        <p style="text-align:center;font-size:0.7rem;color:#cbd5e1;margin-top:1.5rem;">
            © 2024 FinViet Supply Chain. All rights reserved.
        </p>
        """, unsafe_allow_html=True)
