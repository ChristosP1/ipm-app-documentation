"""Interactive HTML/CSS/JS architecture diagram for the home page."""

from __future__ import annotations

from typing import Any

from data.endpoints import ACTOR_ENDPOINTS, ENDPOINTS, ENTITY_FIELDS


def _build_actor_popup_html(actor: str, endpoint_ids: list[str]) -> str:
    """Build popup HTML for a human actor showing grouped endpoints."""
    eps = [e for e in ENDPOINTS if e["id"] in endpoint_ids]
    # Group by subcategory
    groups: dict[str, list[dict[str, Any]]] = {}
    for e in eps:
        sub = e.get("subcategory", "General")
        groups.setdefault(sub, []).append(e)

    sections = ""
    for sub, sub_eps in groups.items():
        links = ""
        for ep in sub_eps:
            m = ep["method"]
            mcls = f"method-{m.lower()}"
            links += (
                f'<a class="popup-endpoint" '
                f'href="/ep-{ep["id"]}" target="_top">'
                f'<span class="mbadge {mcls}">{m}</span> '
                f'<span class="ep-path">{ep["path"]}</span>'
                f"</a>"
            )
        sections += f'<div class="popup-group"><div class="popup-sub">{sub}</div>{links}</div>'

    return (
        f'<div class="popup-title">{actor} Endpoints</div>'
        f'<div class="popup-body">{sections}</div>'
    )


def _build_entity_popup_html(entity: str) -> str:
    """Build popup HTML for a data entity showing Firestore fields."""
    info = ENTITY_FIELDS.get(entity, {})
    path = info.get("firestore_path", "")
    fields = info.get("fields", [])

    rows = ""
    for name, ftype, desc in fields:
        rows += (
            f"<tr>"
            f'<td class="f-name">{name}</td>'
            f'<td class="f-type">{ftype}</td>'
            f'<td class="f-desc">{desc}</td>'
            f"</tr>"
        )

    return (
        f'<div class="popup-title">{entity}</div>'
        f'<div class="popup-path">{path}</div>'
        f'<table class="popup-table">'
        f"<tr><th>Field</th><th>Type</th><th>Description</th></tr>"
        f"{rows}</table>"
    )


def build_diagram_html() -> str:
    """Return self-contained HTML/CSS/JS for the architecture diagram."""

    # Pre-build popup content
    ipm_popup = _build_actor_popup_html("IPM Admin", ACTOR_ENDPOINTS["IPM Admin"])
    ca_popup = _build_actor_popup_html("Client Admin", ACTOR_ENDPOINTS["Client Admin"])
    fac_popup = _build_actor_popup_html("Facilitator", ACTOR_ENDPOINTS["Facilitator"])
    client_popup = _build_entity_popup_html("Client")
    team_popup = _build_entity_popup_html("Team")
    employee_popup = _build_entity_popup_html("Employee")
    meeting_popup = _build_entity_popup_html("Meeting")
    access_popup = _build_entity_popup_html("Access Request")

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter','Segoe UI',system-ui,sans-serif; background:transparent; }}

  .diagram {{ position:relative; width:100%; min-height:620px; padding:20px 10px; }}

  /* ---- Nodes ---- */
  .node {{
    position:absolute;
    border-radius:12px;
    padding:14px 18px;
    text-align:center;
    cursor:pointer;
    transition:transform .15s,box-shadow .15s;
    z-index:2;
    min-width:130px;
  }}
  .node:hover {{ transform:translateY(-3px); box-shadow:0 8px 24px rgba(0,0,0,.15); }}
  .node-actor {{
    background:linear-gradient(135deg,#2563EB,#1D4ED8);
    color:#fff;
    font-weight:600;
    font-size:.92rem;
  }}
  .node-actor .node-sub {{ color:#BFDBFE; font-size:.72rem; font-weight:400; margin-top:2px; }}
  .node-data {{
    background:linear-gradient(135deg,#475569,#334155);
    color:#fff;
    font-weight:600;
    font-size:.88rem;
  }}
  .node-data .node-sub {{ color:#CBD5E1; font-size:.72rem; font-weight:400; margin-top:2px; }}

  /* ---- Arrows (SVG layer) ---- */
  .arrows {{ position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; pointer-events:none; }}
  .arrow-line {{ stroke:#94A3B8; stroke-width:2; fill:none; marker-end:url(#arrowhead); }}
  .arrow-label {{
    font-family:'Inter',sans-serif;
    font-size:11px;
    fill:#64748B;
    text-anchor:middle;
  }}

  /* ---- Popup ---- */
  .popup {{
    display:none;
    position:absolute;
    background:#fff;
    border:1px solid #E2E8F0;
    border-radius:10px;
    box-shadow:0 12px 40px rgba(0,0,0,.18);
    padding:16px;
    z-index:100;
    max-width:480px;
    min-width:320px;
    max-height:400px;
    overflow-y:auto;
  }}
  .popup.visible {{ display:block; }}
  .popup-title {{ font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:4px; }}
  .popup-path {{ font-family:'JetBrains Mono',monospace; font-size:.75rem; color:#64748B; margin-bottom:8px; }}
  .popup-body {{ }}
  .popup-group {{ margin-bottom:8px; }}
  .popup-sub {{ font-size:.78rem; font-weight:600; color:#475569; margin-bottom:3px; border-bottom:1px solid #E2E8F0; padding-bottom:2px; }}

  .popup-endpoint {{
    display:flex; align-items:center; gap:6px;
    padding:3px 6px; border-radius:4px;
    text-decoration:none; color:#334155;
    font-size:.78rem; transition:background .1s;
  }}
  .popup-endpoint:hover {{ background:#F1F5F9; }}
  .mbadge {{
    display:inline-block; padding:1px 6px; border-radius:3px;
    font-weight:700; font-size:.65rem; font-family:'JetBrains Mono',monospace;
    min-width:42px; text-align:center;
  }}
  .method-get {{ background:#DCFCE7; color:#166534; }}
  .method-post {{ background:#DBEAFE; color:#1E40AF; }}
  .method-delete {{ background:#FEE2E2; color:#991B1B; }}
  .ep-path {{ font-family:'JetBrains Mono',monospace; font-size:.72rem; color:#475569; }}

  /* Entity popup table */
  .popup-table {{ width:100%; border-collapse:collapse; font-size:.78rem; }}
  .popup-table th {{ text-align:left; padding:4px 6px; background:#F1F5F9; color:#475569; font-weight:600; border-bottom:2px solid #E2E8F0; }}
  .popup-table td {{ padding:3px 6px; border-bottom:1px solid #E2E8F0; }}
  .f-name {{ font-family:'JetBrains Mono',monospace; color:#1D4ED8; font-size:.75rem; }}
  .f-type {{ font-family:'JetBrains Mono',monospace; color:#64748B; font-size:.72rem; }}
  .f-desc {{ color:#475569; }}

  /* Node positions */
  #n-ipm       {{ left:2%;   top:30px; }}
  #n-client    {{ left:36%;  top:30px; }}
  #n-ca        {{ left:68%;  top:30px; }}
  #n-access    {{ left:2%;   top:200px; }}
  #n-team      {{ left:36%;  top:200px; }}
  #n-employee  {{ left:68%;  top:200px; }}
  #n-meeting   {{ left:36%;  top:380px; }}
  #n-fac       {{ left:68%;  top:380px; }}

</style>
</head>
<body>

<div class="diagram" id="diagram">

  <!-- SVG arrows -->
  <svg class="arrows" id="arrowsSvg">
    <defs>
      <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#94A3B8"/>
      </marker>
    </defs>
  </svg>

  <!-- Actor nodes -->
  <div class="node node-actor" id="n-ipm" data-popup="p-ipm">
    IPM Admin
    <div class="node-sub">Platform administrator</div>
  </div>
  <div class="node node-data" id="n-client" data-popup="p-client">
    Client
    <div class="node-sub">Tenant company</div>
  </div>
  <div class="node node-actor" id="n-ca" data-popup="p-ca">
    Client Admin
    <div class="node-sub">Company administrator</div>
  </div>
  <div class="node node-data" id="n-access" data-popup="p-access">
    Access Request
    <div class="node-sub">Permission workflow</div>
  </div>
  <div class="node node-data" id="n-team" data-popup="p-team">
    Team
    <div class="node-sub">Working group</div>
  </div>
  <div class="node node-data" id="n-employee" data-popup="p-employee">
    Employee
    <div class="node-sub">Team member</div>
  </div>
  <div class="node node-data" id="n-meeting" data-popup="p-meeting">
    Meeting
    <div class="node-sub">Facilitated session</div>
  </div>
  <div class="node node-actor" id="n-fac" data-popup="p-fac">
    Facilitator
    <div class="node-sub">Runs meetings</div>
  </div>

  <!-- Popups -->
  <div class="popup" id="p-ipm">{ipm_popup}</div>
  <div class="popup" id="p-client">{client_popup}</div>
  <div class="popup" id="p-ca">{ca_popup}</div>
  <div class="popup" id="p-access">{access_popup}</div>
  <div class="popup" id="p-team">{team_popup}</div>
  <div class="popup" id="p-employee">{employee_popup}</div>
  <div class="popup" id="p-meeting">{meeting_popup}</div>
  <div class="popup" id="p-fac">{fac_popup}</div>
</div>

<script>
(function() {{
  // Arrow definitions: [fromId, toId, label]
  const arrows = [
    ['n-ipm','n-client','creates'],
    ['n-ipm','n-access','requests access'],
    ['n-client','n-ca','has'],
    ['n-client','n-team','contains'],
    ['n-ca','n-employee','manages'],
    ['n-ca','n-team','manages'],
    ['n-team','n-meeting','has'],
    ['n-employee','n-fac','can be'],
    ['n-fac','n-meeting','creates'],
  ];

  function getCenter(el) {{
    const r = el.getBoundingClientRect();
    const p = el.parentElement.getBoundingClientRect();
    return {{
      x: r.left - p.left + r.width / 2,
      y: r.top - p.top + r.height / 2,
      w: r.width,
      h: r.height
    }};
  }}

  function edgePoint(cx, cy, w, h, tx, ty) {{
    const dx = tx - cx, dy = ty - cy;
    const absDx = Math.abs(dx), absDy = Math.abs(dy);
    const hw = w/2, hh = h/2;
    if (absDx * hh > absDy * hw) {{
      const sign = dx > 0 ? 1 : -1;
      return {{ x: cx + sign * hw, y: cy + (dy * hw) / absDx }};
    }} else {{
      const sign = dy > 0 ? 1 : -1;
      return {{ x: cx + (dx * hh) / absDy, y: cy + sign * hh }};
    }}
  }}

  function drawArrows() {{
    const svg = document.getElementById('arrowsSvg');
    // Clear old arrows
    svg.querySelectorAll('.arrow-g').forEach(g => g.remove());

    arrows.forEach(([fromId, toId, label]) => {{
      const fromEl = document.getElementById(fromId);
      const toEl = document.getElementById(toId);
      if (!fromEl || !toEl) return;

      const from = getCenter(fromEl);
      const to = getCenter(toEl);

      const start = edgePoint(from.x, from.y, from.w, from.h, to.x, to.y);
      const end = edgePoint(to.x, to.y, to.w, to.h, from.x, from.y);

      const g = document.createElementNS('http://www.w3.org/2000/svg','g');
      g.setAttribute('class','arrow-g');

      const line = document.createElementNS('http://www.w3.org/2000/svg','line');
      line.setAttribute('x1', start.x);
      line.setAttribute('y1', start.y);
      line.setAttribute('x2', end.x);
      line.setAttribute('y2', end.y);
      line.setAttribute('class','arrow-line');
      g.appendChild(line);

      if (label) {{
        const text = document.createElementNS('http://www.w3.org/2000/svg','text');
        text.setAttribute('x', (start.x + end.x) / 2);
        text.setAttribute('y', (start.y + end.y) / 2 - 6);
        text.setAttribute('class','arrow-label');
        text.textContent = label;
        g.appendChild(text);
      }}
      svg.appendChild(g);
    }});
  }}

  // Popup logic
  let activePopup = null;
  let hoverNode = null;
  let hoverPopup = false;

  function showPopup(nodeEl) {{
    const popupId = nodeEl.getAttribute('data-popup');
    const popup = document.getElementById(popupId);
    if (!popup) return;
    if (activePopup && activePopup !== popup) activePopup.classList.remove('visible');

    const nr = nodeEl.getBoundingClientRect();
    const dr = nodeEl.parentElement.getBoundingClientRect();
    let left = nr.left - dr.left + nr.width + 12;
    let top = nr.top - dr.top;

    // Keep within diagram bounds
    if (left + 480 > dr.width) left = nr.left - dr.left - 490;
    if (left < 0) left = nr.left - dr.left;
    if (top + 400 > dr.height) top = dr.height - 410;
    if (top < 0) top = 0;

    popup.style.left = left + 'px';
    popup.style.top = top + 'px';
    popup.classList.add('visible');
    activePopup = popup;
  }}

  function hidePopup() {{
    setTimeout(() => {{
      if (!hoverNode && !hoverPopup && activePopup) {{
        activePopup.classList.remove('visible');
        activePopup = null;
      }}
    }}, 150);
  }}

  document.querySelectorAll('.node').forEach(node => {{
    node.addEventListener('mouseenter', () => {{
      hoverNode = node;
      showPopup(node);
    }});
    node.addEventListener('mouseleave', () => {{
      hoverNode = null;
      hidePopup();
    }});
  }});

  document.querySelectorAll('.popup').forEach(popup => {{
    popup.addEventListener('mouseenter', () => {{ hoverPopup = true; }});
    popup.addEventListener('mouseleave', () => {{
      hoverPopup = false;
      hidePopup();
    }});
  }});

  // Draw arrows on load and resize
  drawArrows();
  window.addEventListener('resize', drawArrows);
  // Redraw after a short delay to ensure layout is settled
  setTimeout(drawArrows, 200);
}})();
</script>
</body>
</html>"""
