"""#8004: sending the first message with no conversation open does not await a
second session-list render before the message is posted.

newSession() refreshes the sidebar itself (forced, see #7936). The send path's
nine ``if(!S.session){...}`` branches also awaited renderSessionList(), so the
first message waited for a full /api/sessions + /api/projects read before
POST /api/chat/start. tests/browser_new_chat_focus.py sends a first message with
the list response held.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MESSAGES_JS = (ROOT / "static" / "messages.js").read_text(encoding="utf-8")


def test_the_send_path_creates_the_session_without_awaiting_a_list_render():
    assert "await newSession();await renderSessionList();" not in MESSAGES_JS
    assert MESSAGES_JS.count("if(!S.session){await newSession();}") >= 9
