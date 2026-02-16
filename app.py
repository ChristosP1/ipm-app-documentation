"""IPM Partners Backend – Developer Documentation App.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure the dev_docs package root is on sys.path so imports work
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pages.endpoint_pages import build_endpoint_pages


def main() -> None:
    st.set_page_config(
        page_title="IPM Partners – API Docs",
        page_icon=":material/api:",
        layout="wide",
    )

    # Build per-endpoint pages (49 callable st.Page objects)
    endpoint_page_list, endpoint_page_map = build_endpoint_pages()

    # Store the map so other pages can use st.switch_page(page_object)
    st.session_state["_endpoint_page_map"] = endpoint_page_map

    # Visible pages (shown in top navigation bar)
    visible_pages: dict[str, list[st.Page]] = {
        "": [
            st.Page("pages/home.py", title="Architecture", icon=":material/account_tree:", default=True),
            st.Page("pages/all_endpoints.py", title="All Endpoints", icon=":material/list_alt:"),
            st.Page("pages/processes.py", title="Processes", icon=":material/settings_suggest:"),
        ],
    }

    # Hidden pages (accessible via st.switch_page, NOT shown in nav)
    hidden_pages: dict[str, list[st.Page]] = {
        " ": endpoint_page_list,
    }

    nav = st.navigation(visible_pages | hidden_pages, position="top")
    nav.run()


if __name__ == "__main__":
    main()
