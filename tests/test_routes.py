from app.main import app


def test_create_repository(client):
    payload = {
        "github_url": "https://github.com/octocat/Hello-World",
        "description": "Sample repo"
    }
    response = client.post("/api/repositories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], str)
    assert data["name"] == "octocat/Hello-World"


def test_list_repositories(client):
    response = client.get("/api/repositories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
