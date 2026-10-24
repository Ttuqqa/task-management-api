def get_token(client, username):
    client.post("/register", json={"username": username, "password": "123456"})
    response = client.post("/login", json={"username": username, "password": "123456"})
    return response.get_json()["data"]["token"]

def test_register(client):
    response = client.post("/register", json={"username": "sara", "password": "123456"})
    assert response.status_code == 200
    
def test_login(client):
    client.post("/register", json={"username": "login_user", "password": "123456"})
    response = client.post("/login", json={"username": "login_user", "password": "123456"})
    assert response.status_code == 200
    
def test_create_task(client):
    token = get_token(client, "task_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks", json={"title": "Test task", "due_date": "2026-12-01"}, headers=headers)
    assert response.status_code == 201
    assert response.get_json()["data"]["task_id"] is not None


def test_no_token(client):
    response = client.get("/tasks")
    assert response.status_code == 401


def test_cannot_see_other_users_task(client):
    token_a = get_token(client, "user_a")
    token_b = get_token(client, "user_b")
    created = client.post("/tasks", json={"title": "Private", "due_date": "2026-12-01"}, headers={"Authorization": f"Bearer {token_a}"})
    task_id = created.get_json()["data"]["task_id"]
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert response.status_code == 404