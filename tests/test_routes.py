def test_healthz(client):
    r = client.get("/v1/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    assert r.headers["X-Request-ID"]


def test_word_count(client):
    payload = {"str_input": "hello"}
    r = client.post("/v1/analyses?type=word_count", json=payload)
    assert r.status_code == 200
    assert r.headers["X-Request-ID"]
    assert r.json() == {
        "response": {
            "word_count": str(len(payload["str_input"].split())),
        },
        "message": "ok",
        "request_id": r.headers["X-Request-ID"],
    }


def test_multiple_analyses(client):
    payload = {"str_input": "test semantic analysis"}
    r = client.post(
        "/v1/analyses?type=word_count&type=semantic",
        json=payload,
        headers={"X-Model-Api-Key": "test-api-key"},
    )
    assert r.status_code == 200
    assert r.json() == {
        "response": {
            "word_count": str(len(payload["str_input"].split())),
            "semantic": "'test semantic analysis' is fine",
        },
        "message": "ok",
        "request_id": r.headers["X-Request-ID"],
    }


# def test_partial_failure_does_not_break_response(client):
#     payload = {"str_input": "test semantic analysis"}
#     r = client.post(
#         "/v1/analyses?type=word_count&type=semantic",
#         json=payload,
#     )

#     assert r.status_code == 200
#     assert r.json() == {
#         "response": {
#             "word_count": str(len(payload["str_input"].split())),
#             "semantic": "error: API key required for semantic analysis",
#         },
#         "message": "partial_success",
#         "request_id": r.headers["X-Request-ID"],
#     }


def test_semantic_calls_external(client):
    payload = {"str_input": "test semantic analysis"}
    r = client.post(
        "/v1/analyses?type=semantic",
        json=payload,
        headers={"X-Model-Api-Key": "test-api-key"},
    )

    assert r.status_code == 200
    assert r.json() == {
        "response": {
            "semantic": "'test semantic analysis' is fine",
        },
        "message": "ok",
        "request_id": r.headers["X-Request-ID"],
    }
    assert r.headers["X-Request-ID"]


def test_missing_type_param_returns_422(client):
    payload = {"str_input": "x"}
    r = client.post("/v1/analyses", json=payload)
    assert r.status_code == 422


def test_invalid_type_param_returns_422(client):
    r = client.post("/v1/analyses?type=invalid", json={"str_input": "x"})
    assert r.status_code == 422


def test_empty_input_returns_422(client):
    r = client.post("/v1/analyses?type=word_count", json={"str_input": ""})
    assert r.status_code == 422
