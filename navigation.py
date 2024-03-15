import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("💎 Diamond Corp")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/01_Global_ofertes.py", label="Global ofertes",)
            st.page_link("pages/02_Procedencia_donants_ofertes.py", label="Procedència donants ofertes")
            st.page_link("pages/03_Trasplantaments.py", label="Trasplantaments")
            st.page_link("pages/04_Procedencia_donants_trasplantaments.py", label="Procedència donants trasplantaments")
            st.page_link("pages/05_Rebuig.py", label="Causes Rebuig")
            st.page_link("pages/06_Evolucio.py", label="Evolució")


            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "login":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("login.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("login.py")