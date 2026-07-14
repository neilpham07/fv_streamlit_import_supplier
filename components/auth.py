import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

_APP_USER = os.getenv("APP_USERNAME")
_APP_PASS = os.getenv("APP_PASSWORD")
if not _APP_USER or not _APP_PASS:
    raise RuntimeError("APP_USERNAME and APP_PASSWORD must be set in environment variables.")

_USERS = {_APP_USER: _APP_PASS}

_MAX_ATTEMPTS = 5
_LOCKOUT_SECONDS = 300  # 5 minutes


def login_page():
    import time
    st.markdown("""
    <style>
    .block-container { padding-top: 4vh !important; }
    body { background: #f1f5f9; }
    </style>
    """, unsafe_allow_html=True)

    # ── Rate limiting ─────────────────────────────────────────────────────────
    now = time.time()
    attempts   = st.session_state.get("login_attempts", 0)
    locked_at  = st.session_state.get("login_locked_at", 0)

    if attempts >= _MAX_ATTEMPTS:
        remaining = int(_LOCKOUT_SECONDS - (now - locked_at))
        if remaining > 0:
            st.error(f"Too many failed attempts. Please wait {remaining} seconds.")
            st.stop()
        else:
            st.session_state.login_attempts = 0
            st.session_state.login_locked_at = 0

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
                st.session_state.login_attempts = 0
                st.rerun()
            else:
                st.session_state.login_attempts = attempts + 1
                if st.session_state.login_attempts >= _MAX_ATTEMPTS:
                    st.session_state.login_locked_at = time.time()
                st.error("Invalid credentials. Please try again.")

        st.markdown("""
        <p style="text-align:center;font-size:0.7rem;color:#cbd5e1;margin-top:1.5rem;">
            © 2024 FinViet Supply Chain. All rights reserved.
        </p>
        """, unsafe_allow_html=True)
