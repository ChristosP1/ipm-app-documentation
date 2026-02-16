"""Processes & Pipelines -- documents the complex backend workflows."""

from __future__ import annotations

import streamlit as st

from components.styles import inject_global_css

inject_global_css()

# ---------------------------------------------------------------------------
# Helper: render a numbered process step using the global CSS classes
# ---------------------------------------------------------------------------

def _step(number: int, text: str) -> str:
    """Return HTML for a single process-step card."""
    return (
        f'<div class="process-step">'
        f'<div class="process-step-number">{number}</div>'
        f"<div>{text}</div>"
        f"</div>"
    )


def _steps(items: list[str]) -> None:
    """Render a sequence of process steps."""
    html = "".join(_step(i, t) for i, t in enumerate(items, 1))
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("Processes & Pipelines")
st.markdown(
    "Deep-dive into every major backend workflow -- from audio ingestion to "
    "AI-powered analysis and permission management. Each tab covers a single "
    "process end-to-end: the trigger, intermediate steps, external services "
    "involved, and the final artefacts produced."
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_diarization, tab_recognition, tab_auth, tab_analysis, tab_access = st.tabs(
    [
        "Diarization",
        "Speaker Recognition",
        "Authentication",
        "Meeting Analysis",
        "Access Requests",
    ]
)

# ===== TAB 1: Diarization ===================================================
with tab_diarization:
    st.markdown('<div class="tag-header">Speaker Diarization via WhisperX + pyannote</div>', unsafe_allow_html=True)
    st.markdown(
        "Speaker diarization segments an audio recording into time-stamped, "
        "speaker-labelled sections using **WhisperX** for transcription and "
        "**pyannote** for speaker assignment."
    )

    st.markdown("#### Pipeline Flow")
    _steps(
        [
            "Audio file uploaded (<code>mp3</code> / <code>wav</code> only).",
            "WhisperX model loaded (cached with <code>@lru_cache</code>, auto GPU / CPU detection).",
            "WhisperX transcribes audio with <b>word-level timestamps</b>.",
            "pyannote assigns speaker labels (<code>SPEAKER_00</code>, <code>SPEAKER_01</code>, ...).",
            "Per-speaker audio extracted using <b>pydub</b> (group segments, slice, concatenate).",
            "Each speaker's audio trimmed to a <b>10 s</b> preview and <b>base64-encoded</b> as WAV.",
            "Diarized transcript JSON saved to <b>Firebase Storage</b>.",
            "Meeting document updated with <code>transcript_storage_path</code>.",
        ]
    )

    st.markdown("#### Technical Details")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**GPU (CUDA)**")
        st.markdown(
            """
- Device: `cuda`
- Batch size: **16**
- Compute type: `float16`
"""
        )
    with col2:
        st.markdown("**CPU fallback**")
        st.markdown(
            """
- Device: `cpu`
- Batch size: **8**
- Compute type: `int8`
"""
        )

    st.warning("Device selection is automatic -- CUDA is preferred when available; the service falls back to CPU transparently.")

    st.markdown("#### Output Structure")
    st.code(
        """{
  "segments": [
    { "start": 0.0, "end": 3.42, "text": "Hello everyone.", "speaker": "SPEAKER_00" },
    { "start": 3.50, "end": 7.81, "text": "Welcome to the meeting.", "speaker": "SPEAKER_01" }
  ],
  "speakers": {
    "SPEAKER_00": { "audio_preview": "<base64>" },
    "SPEAKER_01": { "audio_preview": "<base64>" }
  }
}""",
        language="json",
    )

    st.markdown("#### Endpoint")
    st.code("POST /facilitator/meetings/{meeting_id}/diarize", language="http")

    with st.expander("Source code reference"):
        st.markdown(
            "`services/ipm_app/diarization_service.py` -- WhisperX loading, "
            "transcription, pyannote diarization, pydub audio slicing, and Storage persistence."
        )

# ===== TAB 3: Speaker Recognition ===========================================
with tab_recognition:
    st.markdown('<div class="tag-header">Speaker Recognition via SpeechBrain + Hungarian Algorithm</div>', unsafe_allow_html=True)
    st.markdown(
        "Voice biometric matching identifies **who** each diarized speaker is by "
        "comparing their voice embeddings against known employee embeddings. Uses "
        "**SpeechBrain ECAPA-VoxCeleb** for encoding and the **Hungarian algorithm** "
        "for optimal one-to-one assignment."
    )

    st.markdown("#### Full Diarize-and-Identify Pipeline")
    _steps(
        [
            "Diarization runs (same pipeline as the Diarization tab).",
            "Per-speaker audio segments extracted.",
            "Audio normalized to <b>mono 16 kHz WAV</b> (<code>audio_preprocessing_service</code>).",
            "SpeechBrain <b>ECAPA-VoxCeleb</b> encoder creates an embedding per speaker: audio chunked "
            "(configurable chunk seconds), silent chunks filtered (RMS threshold), chunks encoded, "
            "averaged, and <b>L2-normalized</b>.",
            "Speaker embeddings JSON saved to <b>Firebase Storage</b>.",
            "Participant embeddings loaded from Storage (uploaded earlier by the client admin).",
            "Similarity matrix built: <code>(n_speakers x n_employees)</code>, cosine similarity via dot product.",
            "<code>scipy.optimize.linear_sum_assignment</code> (<b>Hungarian algorithm</b>) finds optimal 1-to-1 matching.",
            "Matches below the confidence threshold are marked <b>unmatched</b> (<code>employee_id = null</code>).",
        ]
    )

    st.markdown("#### Speaker Confirmation Flow")
    st.info(
        "After automatic matching, the facilitator reviews and confirms speaker "
        "identities. Confirmed assignments update the transcript with real names and "
        "persist speaker embeddings to the employee's storage path for future matching improvements."
    )
    st.code("POST /facilitator/meetings/{meeting_id}/confirm-speakers", language="http")

    st.markdown("#### Voice Embedding Upload")
    st.markdown(
        "Client admins can upload voice samples for employees ahead of time so the "
        "matching pipeline has reference embeddings to compare against."
    )
    st.code("POST /client-admin/employees/{employee_id}/voice-embeddings", language="http")

    st.markdown("#### Primary Endpoint")
    st.code("POST /facilitator/meetings/{meeting_id}/diarize-and-identify", language="http")

    with st.expander("Embedding creation details"):
        st.markdown(
            """
1. Raw audio is preprocessed to **mono 16 kHz WAV**.
2. The waveform is split into chunks of configurable length.
3. Chunks whose RMS energy falls below a silence threshold are discarded.
4. Remaining chunks are fed through the **ECAPA-TDNN** encoder.
5. Resulting chunk embeddings are averaged and **L2-normalized** to produce a single fixed-length vector.
"""
        )

    with st.expander("Matching algorithm details"):
        st.markdown(
            """
- A **cosine similarity matrix** of shape `(n_speakers, n_employees)` is computed via dot product (embeddings are already L2-normalized).
- The matrix is negated and passed to `scipy.optimize.linear_sum_assignment` which solves the assignment problem in **O(n^3)** using the Hungarian algorithm.
- Each resulting pair is checked against a configurable **confidence threshold**; pairs below the threshold are returned with `employee_id = null`.
"""
        )

    with st.expander("Source code references"):
        st.markdown(
            """
- `services/ipm_app/embedding_creation_service.py` -- ECAPA-VoxCeleb encoding, chunking, normalization.
- `services/ipm_app/speaker_matching_service.py` -- similarity matrix, Hungarian matching, threshold filtering.
- `services/ipm_app/audio_preprocessing_service.py` -- resampling, mono conversion, format normalization.
"""
        )

# ===== TAB 4: Authentication ================================================
with tab_auth:
    st.markdown('<div class="tag-header">Three-Tier Authentication System</div>', unsafe_allow_html=True)
    st.markdown(
        "The backend uses three distinct authentication mechanisms depending on the "
        "actor type. Each tier has its own token format, header convention, and "
        "dependency chain."
    )

    # --- Tier 1 ---------------------------------------------------------------
    st.markdown("---")
    st.markdown("### Tier 1 -- IPM Admin / Client Admin (Firebase Auth)")
    st.markdown(
        """
- **Method:** Firebase Auth email + password login.
- **Endpoint:** `POST /global/admin/login` returns a Firebase ID token.
- **Token delivery:** `Authorization: Bearer {firebase_id_token}` header.
- **Dependency chain:** `require_firebase_auth` validates the token, then either
  `require_ipm_admin` or `require_client_admin` asserts the correct role.
"""
    )
    st.code(
        """\
# Example request
POST /global/admin/login
Content-Type: application/json

{ "email": "admin@example.com", "password": "••••••••" }

# Response includes Firebase ID token
# Subsequent requests:
GET /ipm-admin/clients
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...""",
        language="http",
    )

    # --- Tier 2 ---------------------------------------------------------------
    st.markdown("---")
    st.markdown("### Tier 2 -- Facilitator (QR + PIN)")
    _steps(
        [
            "Client admin creates a team -- an <code>access_link_id</code> (UUID) is generated and "
            "embedded into a <b>JWT</b> (HS256, <b>365-day</b> TTL).",
            "A <b>QR code</b> is created encoding a URL that contains the JWT.",
            "Facilitator scans the QR code and sends the JWT in the <code>X-Access-Token</code> header "
            "along with their PIN in the request body.",
            "Backend verifies the JWT, looks up the employee by PIN (<b>bcrypt</b>, 12 rounds).",
            "A <b>session JWT</b> (24 h TTL) is issued containing <code>facilitator_id</code>, "
            "<code>team_id</code>, <code>client_id</code>, and <code>access_link_id</code>.",
            "Session token is used as the <code>X-Team-Session</code> header for all subsequent facilitator requests.",
        ]
    )
    st.warning(
        "The QR JWT has a **365-day** lifetime -- it acts as a long-lived team "
        "invitation. The session JWT issued after PIN verification expires after "
        "**24 hours**."
    )

    # --- Tier 3 ---------------------------------------------------------------
    st.markdown("---")
    st.markdown("### Tier 3 -- Access Permission Flow")
    st.markdown(
        """
- An **IPM admin** requests access to a specific client's data.
- The **client admin** accepts the request.
- The dependency `require_ipm_admin_with_client_access` enforces that the IPM admin
  has an **ACCEPTED** access request for the target client before granting access.
"""
    )

    # --- Header reference ------------------------------------------------------
    st.markdown("---")
    st.markdown("### Header Reference")
    st.markdown(
        """
| Header | Value | Used By |
|--------|-------|---------|
| `Authorization` | `Bearer {firebase_id_token}` | Admin endpoints (IPM / Client) |
| `X-Access-Token` | `{qr_jwt}` | Session creation (facilitator login) |
| `X-Team-Session` | `{session_jwt}` | Facilitator endpoints |
| `X-Client-ID` | `{client_id}` | Some IPM admin endpoints |
"""
    )

    with st.expander("Dependency chain summary"):
        st.markdown(
            """
```
require_firebase_auth          -- validates Firebase ID token
  require_ipm_admin            -- asserts IPM admin role
  require_client_admin         -- asserts client admin role
  require_ipm_admin_with_client_access
                                -- IPM admin + ACCEPTED access request for target client

require_team_session           -- validates session JWT (X-Team-Session)
```
"""
        )

# ===== TAB 4: Meeting Analysis ==============================================
with tab_analysis:
    st.markdown('<div class="tag-header">AI-Powered Meeting Analysis via Gemini</div>', unsafe_allow_html=True)
    st.markdown(
        "Once a meeting has been **diarized** (via `/diarize` or `/diarize-and-identify`), "
        "the backend can run an **AI analysis** using Google Gemini to score team maturity "
        "across eight categories and identify the three most relevant facilitator competencies."
    )

    st.markdown("#### Pipeline Flow")
    _steps(
        [
            "Diarized transcript JSON files fetched from <b>Firebase Storage</b> "
            "(<code>clients/{client_id}/teams/{team_id}/meetings/{meeting_id}/diarized_transcript*.json</code>).",
            "Each JSON's segments parsed into <b>chat format</b>: <code>- Speaker Name: sentence</code>.",
            "Multiple JSON files are sorted by name and concatenated.",
            "Gemini runs <b>category analysis</b>: 8 team maturity categories scored 1 -- 4.",
            "Gemini runs <b>competency analysis</b>: 3 most relevant facilitator competencies selected.",
            "Results stored in the meeting document in Firestore.",
        ]
    )

    st.markdown("#### Category Scoring (Team Maturity)")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric(label="Initial", value="1")
    with col_b:
        st.metric(label="Developing", value="2")
    with col_c:
        st.metric(label="Established", value="3")
    with col_d:
        st.metric(label="Advanced", value="4")

    st.markdown(
        "Each of the **8 categories** receives a score from 1 to 4 along with a "
        "textual **explanation** and actionable **suggestions** for improvement."
    )

    st.markdown("#### Competency Analysis (Facilitator)")
    st.markdown(
        """
- **3 competencies** are selected from a pool of **25** predefined competencies.
- Each selected competency includes:
  - A qualitative **assessment** of the facilitator's performance.
  - A **priority** level: `high`, `medium`, or `low`.
  - Concrete **feedback** for professional development.
"""
    )

    st.info(
        "Both analysis passes use the same diarized transcript (formatted as a chat log) "
        "but independent Gemini prompts to keep category and competency evaluation decoupled."
    )

    st.markdown("#### Endpoint")
    st.code("POST /facilitator/meetings/{meeting_id}/analyze", language="http")

    with st.expander("Source code reference"):
        st.markdown(
            "`services/ipm_app/transcript_analysis_service.py` -- prompt construction, "
            "Gemini API calls, response parsing, and Firestore persistence."
        )

# ===== TAB 6: Access Requests ===============================================
with tab_access:
    st.markdown('<div class="tag-header">Access Request Permission Workflow</div>', unsafe_allow_html=True)
    st.markdown(
        "Access requests govern how **IPM admins** gain permission to view or manage "
        "a specific **client's** data. The workflow follows a strict state machine "
        "with clear ownership of each transition."
    )

    st.markdown("#### State Machine")
    st.code(
        """\
                      
          PENDING ── {accept} ──► ACCEPTED
            │                        │
        {decline}                 {revoke}                            
            │                        │ 
            ▼                        ▼
         DECLINED                 REVOKED

        PENDING  ── {delete} ──►  (removed)""",
        language="text",
    )

    st.markdown("#### Workflow Steps")
    _steps(
        [
            "IPM admin creates an access request for a target client.",
            "Client admin reviews pending requests.",
            "Client admin <b>accepts</b>, <b>declines</b>, or later <b>revokes</b> the request.",
            "Once <b>ACCEPTED</b>, the IPM admin can access the client's data via "
            "<code>require_ipm_admin_with_client_access</code>.",
        ]
    )

    st.markdown("#### Available Actions by Role")

    col_ipm, col_client = st.columns(2)
    with col_ipm:
        st.markdown("**IPM Admin**")
        st.markdown(
            """
- **Create** a new access request
  `POST /ipm-admin/access-requests`
- **Delete** a pending request
  `DELETE /ipm-admin/access-requests/{id}`
- **List** own requests
  `GET /ipm-admin/access-requests`
"""
        )
    with col_client:
        st.markdown("**Client Admin**")
        st.markdown(
            """
- **List** incoming requests
  `GET /client-admin/access-requests`
- **Accept** a request
  `POST /client-admin/access-requests/{id}/accept`
- **Decline** a request
  `POST /client-admin/access-requests/{id}/decline`
- **Revoke** a previously accepted request
  `POST /client-admin/access-requests/{id}/revoke`
"""
        )

    st.info(
        "Only requests in the **ACCEPTED** state grant data access. Declined and "
        "revoked requests are retained for audit purposes but confer no permissions."
    )

    with st.expander("Source code references"):
        st.markdown(
            """
- `routers/ipm_admin.py` -- IPM admin endpoints for creating, listing, and deleting access requests.
- `routers/client_admin.py` -- Client admin endpoints for reviewing and actioning requests.
"""
        )
