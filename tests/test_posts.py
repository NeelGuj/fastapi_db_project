import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200



def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']



def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/50")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")    #test_posts[3] is post number 4, created by test_user2.
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']



def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id      # Authorized user 1(test_user) is trying to update post created by user 2(test_user2).

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403



def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/50", json=data)

    assert res.status_code == 404


def test_unauthorized_user_patch_post(client, test_user, test_posts):
    data = {"title": "patched title"}
    res = client.patch(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_patch_post_non_exist(authorized_client, test_user, test_posts):
    data = {"title": "patched title"}
    res = authorized_client.patch(f"/posts/99999", json=data)
    assert res.status_code == 404
    

# Verifies that an authorized user can successfully patch their own post.
def test_patch_post_success(authorized_client, test_user, test_posts):
    data = {"title": "patched title"}
    res = authorized_client.patch(f"/posts/{test_posts[0].id}", json=data)
    patched_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert patched_post.title == data["title"]
    assert patched_post.content == test_posts[0].content  # Content should remain unchanged


def test_patch_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {"title": "patched title"}
    res = authorized_client.patch(f"/posts/{test_posts[3].id}", json=data)  # Post owned by test_user2
    assert res.status_code == 403


#  Confirms that only the specified fields are updated, while others remain unchanged.
def test_patch_post_partial_update(authorized_client, test_user, test_posts):
    data = {"content": "patched content"}
    res = authorized_client.patch(f"/posts/{test_posts[0].id}", json=data)
    patched_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert patched_post.content == data["content"]
    assert patched_post.title == test_posts[0].title  # Title should remain unchanged


