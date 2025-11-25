from app import schemas, models


def test_create_post(authorised_client):
    response = authorised_client.post(
        "/posts/",
        json={"title": "Test", "content": "Hello world"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test"


def test_get_all_posts(authorised_client, test_posts):
    response = authorised_client.get("/posts/")
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_unauthorized_get_all_posts(client, test_posts):
    resp = client.get("/posts/")
    assert resp.status_code == 401


def test_get_one_post(authorised_client, test_posts):
    post = test_posts[0]
    response = authorised_client.get(f"/posts/{post.id}")
    assert response.status_code == 200
    parsed = schemas.PostOut(**response.json())
    assert parsed.Post.id == post.id


def test_get_one_post_not_exist(authorised_client):
    resp = authorised_client.get("/posts/999999")
    assert resp.status_code == 404
