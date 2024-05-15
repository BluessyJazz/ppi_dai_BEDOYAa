import streamlit as st
from typing import Optional

from modules.auth.authenticate import Authenticate


def authenticated_menu(auth):
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/prueba.py", label="Manage users")
    # st.sidebar.page_link(
    #    "pages/autentica2.py",
    #    label="Manage admin access",
    #    disabled=st.session_state.authentication_status != "super-admin",
    # )

    c = st.sidebar.empty()

    c.write("")

    auth.logout(location='sidebar')


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("pages/iniciar_sesion.py", label="Iniciar sesión 🔐")
    st.sidebar.page_link("pages/registrarse.py", label="Registrarse 📝")


def menu(auth: Optional[Authenticate] = None):
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    st.sidebar.page_link("main.py", label="Wily MotoTrack :racing_motorcycle:")

    if auth is None:
        unauthenticated_menu()
        return None

    elif auth == 'ok':
        return auth
    else:
        authenticated_menu(auth)


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    # if "role" not in st.session_state or st.session_state.role is None:
    #    st.switch_page("app.py")
    # menu()
    pass
