import json
from http import HTTPStatus

from hafiz_ai.web.app import HafizWebApp

app = HafizWebApp()


def test_list_passages_returns_metadata():
    status, headers, body = app.dispatch("GET", "/api/v1/passages", b"")
    assert status == HTTPStatus.OK
    assert headers["Content-Type"].startswith("application/json")
    payload = json.loads(body.decode("utf-8"))
    assert isinstance(payload, list)
    assert payload, "At least one passage should be available"
    first = payload[0]
    assert {"id", "surah", "arabic_text", "transliteration"}.issubset(first)


def test_evaluate_endpoint_scores_transcript():
    passages = json.loads(app.list_passages())
    passage_id = passages[0]["id"]
    transcript = passages[0]["arabic_text"]
    payload = json.dumps({"passage_id": passage_id, "transcript": transcript}).encode("utf-8")

    status, _, body = app.dispatch("POST", "/api/v1/evaluate", payload)
    assert status == HTTPStatus.OK
    feedback = json.loads(body.decode("utf-8"))
    assert feedback["accuracy_score"] == 100.0
    assert feedback["missing_words"] == []
    assert feedback["extra_words"] == []
