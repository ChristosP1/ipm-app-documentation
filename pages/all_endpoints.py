"""All Endpoints page – categorized listing of every API endpoint."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.styles import inject_global_css, method_badge_html
from data.endpoints import ENDPOINTS, TAG_DISPLAY_NAMES, TAG_ORDER


def _get_subcategories(endpoints: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group endpoints by subcategory, preserving insertion order."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for ep in endpoints:
        sub = ep.get("subcategory", "General")
        groups.setdefault(sub, []).append(ep)
    return groups


def _method_counts(endpoints: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for ep in endpoints:
        m = ep["method"]
        counts[m] = counts.get(m, 0) + 1
    return counts


inject_global_css()

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("All Endpoints")
st.markdown(
    "Complete reference of every API endpoint, organised by category and sub-category. "
    "Click **View details** on any endpoint to see its full documentation."
)

# ---------------------------------------------------------------------------
# Quick stats
# ---------------------------------------------------------------------------
counts = _method_counts(ENDPOINTS)
pills = "".join(
    f'<span class="stat-pill">'
    f'{method_badge_html(m)} {c}'
    f"</span>"
    for m, c in sorted(counts.items())
)
st.markdown(
    f'<div style="margin:8px 0 18px 0;">'
    f'<span class="stat-pill" style="background:#2563EB;color:white;">'
    f"Total: {len(ENDPOINTS)}</span> {pills}</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Search / filter
# ---------------------------------------------------------------------------
col_search, col_method = st.columns([3, 1])
with col_search:
    search = st.text_input(
        "Search endpoints",
        placeholder="Type to filter by path, title, or description…",
        label_visibility="collapsed",
    )
with col_method:
    method_filter = st.selectbox(
        "Method",
        ["All", "GET", "POST", "DELETE", "PUT", "PATCH"],
        label_visibility="collapsed",
    )

search_lower = search.strip().lower()


def _matches(ep: dict[str, Any]) -> bool:
    if method_filter != "All" and ep["method"] != method_filter:
        return False
    if search_lower:
        haystack = f"{ep['path']} {ep['title']} {ep.get('summary', '')} {ep.get('description_long', '')}".lower()
        return search_lower in haystack
    return True


filtered = [ep for ep in ENDPOINTS if _matches(ep)]

if not filtered:
    st.info("No endpoints match your search.")
    st.stop()

# ---------------------------------------------------------------------------
# Render by tag → subcategory
# ---------------------------------------------------------------------------
# Determine which tags are present in filtered results
present_tags = []
for tag in TAG_ORDER:
    if any(ep["tag"] == tag for ep in filtered):
        present_tags.append(tag)
# Include any tags not in TAG_ORDER
for ep in filtered:
    if ep["tag"] not in present_tags:
        present_tags.append(ep["tag"])

for tag in present_tags:
    tag_endpoints = [ep for ep in filtered if ep["tag"] == tag]
    if not tag_endpoints:
        continue

    display_name = TAG_DISPLAY_NAMES.get(tag, tag)
    st.markdown(
        f'<div class="tag-header">{display_name} '
        f'<span style="font-size:0.8rem;font-weight:400;color:#64748B;">({len(tag_endpoints)} endpoints)</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    subcategories = _get_subcategories(tag_endpoints)

    for sub_name, sub_eps in subcategories.items():
        st.markdown(
            f'<div class="subcategory-header">{sub_name}</div>',
            unsafe_allow_html=True,
        )

        for ep in sub_eps:
            badge = method_badge_html(ep["method"])
            auth_html = (
                f'<span class="auth-badge">{ep["auth"]}</span>'
                if ep.get("auth")
                else ""
            )

            st.markdown(
                f"""<div class="endpoint-card">
                    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                        {badge}
                        <span class="endpoint-path">{ep["path"]}</span>
                        {auth_html}
                    </div>
                    <div style="margin-top:6px;font-size:0.92rem;font-weight:600;color:#0F172A;">
                        {ep["title"]}
                    </div>
                    <div style="margin-top:2px;font-size:0.82rem;color:#64748B;">
                        {ep.get("summary", "")}
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

            if st.button(
                "View details",
                key=f"all_{ep['id']}",
                type="tertiary",
                icon=":material/arrow_forward:",
            ):
                page_map = st.session_state.get("_endpoint_page_map", {})
                target_page = page_map.get(ep["id"])
                if target_page:
                    st.switch_page(target_page)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
