# tests/test_crud.py
"""Basic integration tests for CRUD operations using Flask test client."""

import json

def test_create_and_get_student(client):
    # Create student via JSON API
    payload = {
        "enrollment_no": "ENR001",
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "course": "CSE"
    }
    resp = client.post("/api/students", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["enrollment_no"] == "ENR001"
    student_id = data["id"]

    # Fetch student
    get_resp = client.get(f"/api/students/{student_id}")
    assert get_resp.status_code == 200
    got = get_resp.get_json()
    assert got["first_name"] == "Alice"

def test_update_and_delete_student(client):
    # Create student
    payload = {"enrollment_no": "ENR002", "first_name": "Bob"}
    resp = client.post("/api/students", json=payload)
    assert resp.status_code == 201
    sid = resp.get_json()["id"]

    # Update
    update = {"first_name": "Bobby", "email": "bob@example.com"}
    put = client.put(f"/api/students/{sid}", json=update)
    assert put.status_code == 200
    assert put.get_json()["first_name"] == "Bobby"
    assert put.get_json()["email"] == "bob@example.com"

    # Delete
    del_resp = client.delete(f"/api/students/{sid}")
    assert del_resp.status_code == 204

    # Ensure gone
    get_resp = client.get(f"/api/students/{sid}")
    assert get_resp.status_code == 404
