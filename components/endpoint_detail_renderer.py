"""Shared rendering logic for a single endpoint detail page."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.styles import inject_global_css, method_badge_html, status_code_html
from data.endpoints import ENDPOINTS


def render_endpoint_detail(ep: dict[str, Any]) -> None:
    """Render the full documentation view for a single endpoint."""
    inject_global_css()

    # Back button
    if st.button("Back to All Endpoints", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("pages/all_endpoints.py")

    # Header
    badge = method_badge_html(ep["method"])
    st.markdown(
        f'<div style="margin-top:8px;">{badge} '
        f'<span class="endpoint-path" style="font-size:1.15rem;">{ep["path"]}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"## {ep['title']}")

    # Meta row
    meta_parts = []
    if ep.get("auth"):
        meta_parts.append(f'<span class="auth-badge">{ep["auth"]}</span>')
    meta_parts.append(
        f'<span style="font-size:0.78rem;color:#64748B;">'
        f'{ep.get("source_file", "")}:{ep.get("source_line", "")}</span>'
    )
    st.markdown(
        f'<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:8px;">'
        + " ".join(meta_parts)
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Description
    desc = ep.get("description_long", ep.get("summary", ""))
    if desc:
        st.markdown("### Description")
        st.markdown(desc)

    # Path parameters
    path_params: list[tuple[str, str, str]] = ep.get("path_params", [])
    if path_params:
        st.markdown("### Path Parameters")
        rows = "".join(
            f'<tr><td class="field-name">{name}</td>'
            f'<td class="field-type">{ftype}</td>'
            f"<td>{fdesc}</td></tr>"
            for name, ftype, fdesc in path_params
        )
        st.markdown(
            f'<table class="schema-table"><thead><tr>'
            f"<th>Name</th><th>Type</th><th>Description</th>"
            f"</tr></thead><tbody>{rows}</tbody></table>",
            unsafe_allow_html=True,
        )

    # Query parameters
    query_params: list[tuple[str, str, str]] = ep.get("query_params", [])
    if query_params:
        st.markdown("### Query Parameters")
        rows = "".join(
            f'<tr><td class="field-name">{name}</td>'
            f'<td class="field-type">{ftype}</td>'
            f"<td>{fdesc}</td></tr>"
            for name, ftype, fdesc in query_params
        )
        st.markdown(
            f'<table class="schema-table"><thead><tr>'
            f"<th>Name</th><th>Type</th><th>Description</th>"
            f"</tr></thead><tbody>{rows}</tbody></table>",
            unsafe_allow_html=True,
        )

    # Request body
    request_body: list[tuple[str, ...]] = ep.get("request_body", [])
    if request_body:
        st.markdown("### Request Body")
        rows = ""
        for item in request_body:
            if len(item) == 4:
                name, ftype, required, fdesc = item
                req_text = "Yes" if required else "No"
            else:
                name, ftype, fdesc = item[0], item[1], item[-1]
                req_text = "-"
            rows += (
                f'<tr><td class="field-name">{name}</td>'
                f'<td class="field-type">{ftype}</td>'
                f"<td>{req_text}</td>"
                f"<td>{fdesc}</td></tr>"
            )
        st.markdown(
            f'<table class="schema-table"><thead><tr>'
            f"<th>Field</th><th>Type</th><th>Required</th><th>Description</th>"
            f"</tr></thead><tbody>{rows}</tbody></table>",
            unsafe_allow_html=True,
        )

    # Response
    response_fields: list[tuple[str, str, str]] = ep.get("response_fields", [])
    if response_fields:
        resp_status = ep.get("response_status", 200)
        st.markdown(f"### Response ({resp_status})")
        rows = "".join(
            f'<tr><td class="field-name">{name}</td>'
            f'<td class="field-type">{ftype}</td>'
            f"<td>{fdesc}</td></tr>"
            for name, ftype, fdesc in response_fields
        )
        st.markdown(
            f'<table class="schema-table"><thead><tr>'
            f"<th>Field</th><th>Type</th><th>Description</th>"
            f"</tr></thead><tbody>{rows}</tbody></table>",
            unsafe_allow_html=True,
        )

    # Status codes
    status_codes: dict[int, str] = ep.get("status_codes", {})
    if status_codes:
        st.markdown("### Status Codes")
        rows = "".join(
            f"<tr><td>{status_code_html(code)}</td><td>{fdesc}</td></tr>"
            for code, fdesc in sorted(status_codes.items())
        )
        st.markdown(
            f'<table class="schema-table"><thead><tr>'
            f"<th>Code</th><th>Description</th>"
            f"</tr></thead><tbody>{rows}</tbody></table>",
            unsafe_allow_html=True,
        )

    # Related endpoints (for complex ones)
    complexity = ep.get("complexity", "simple")
    if complexity == "complex":
        related = [
            e
            for e in ENDPOINTS
            if e["tag"] == ep["tag"]
            and e["subcategory"] == ep["subcategory"]
            and e["id"] != ep["id"]
        ]
        if related:
            st.markdown("### Related Endpoints")
            for rel in related:
                rel_badge = method_badge_html(rel["method"])
                st.markdown(
                    f'{rel_badge} `{rel["path"]}` — {rel["title"]}',
                    unsafe_allow_html=True,
                )
