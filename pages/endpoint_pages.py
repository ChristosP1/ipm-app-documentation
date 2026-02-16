"""Programmatic generation of st.Page objects for all endpoints."""

from __future__ import annotations

import streamlit as st

from components.endpoint_detail_renderer import render_endpoint_detail
from data.endpoints import ENDPOINTS, get_endpoint_by_id


def _make_page_fn(endpoint_id: str):
    """Return a closure that renders the detail page for a specific endpoint."""

    def _page():
        ep = get_endpoint_by_id(endpoint_id)
        if not ep:
            st.error("Endpoint not found.")
            st.stop()
        render_endpoint_detail(ep)

    return _page


def build_endpoint_pages() -> tuple[list[st.Page], dict[str, st.Page]]:
    """Build st.Page objects for all endpoints.

    Returns:
        (pages_list, pages_by_id) — pages_by_id maps endpoint_id → st.Page
    """
    pages: list[st.Page] = []
    by_id: dict[str, st.Page] = {}
    for ep in ENDPOINTS:
        page = st.Page(
            _make_page_fn(ep["id"]),
            title=ep["title"],
            url_path=f"ep-{ep['id']}",
        )
        pages.append(page)
        by_id[ep["id"]] = page
    return pages, by_id
