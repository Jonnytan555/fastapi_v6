import pytest
from app import schemas


# ---------------------------------------------------------
#  Get Tests
# ---------------------------------------------------------

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


# ---------------------------------------------------------
#  Create Tests
# ---------------------------------------------------------

@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome content", True),
        ("favourite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", True),
    ]
)
def test_create_post(authorised_client, test_user, title, content, published):
    response = authorised_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published(authorised_client, test_user, test_posts):
    response = authorised_client.post(
        "/posts/",
        json={"title": "arbitrary title", "content": "asdfdg", "published": True}
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "asdfdg"
    assert created_post.published is True
    assert created_post.user_id == test_user["id"]


def test_unauthorised_create_post(client, test_user, test_posts):
    response = client.post(
        "/posts/",
        json={"title": "arbitrary title", "content": "asdfdg", "published": True}
    )
    assert response.status_code == 401


# ---------------------------------------------------------
#  Delete Tests
# ---------------------------------------------------------

def test_delete_post_success(authorised_client, test_user, test_posts):
    response = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_unauthorised_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_non_exist(client, test_user, test_posts):
    response = client.delete(f"/posts/80000000000")
    assert response.status_code == 401


def test_delete_other_user_post(authorised_client, test_user, test_posts):
    response = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


# ---------------------------------------------------------
#  Update Tests
# ---------------------------------------------------------

def test_update_other_user_post(authorised_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    response = authorised_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403


def test_unauthorised_update_post(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_update_post_non_exist(authorised_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    response = authorised_client.put(f"/posts/800000000", json=data)
    assert response.status_code == 404


# ---------------------------------------------------------
#  Vote Tests
# ---------------------------------------------------------

def test_vote_on_post(authorised_client, test_posts):
    response = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == 201


def test_vote_twice_on_post(authorised_client, test_posts, test_vote):
    response = authorised_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 409


def test_delete_vote_non_exists(authorised_client, test_posts):
    response = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert response.status_code == 404


def test_vote_non_exists(authorised_client, test_posts):
    response = authorised_client.post("/vote/", json={"post_id": 80000000, "dir": 0})
    assert response.status_code == 404


def test_vote_unauthorised_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": 80000000, "dir": 0})
    assert response.status_code == 401
