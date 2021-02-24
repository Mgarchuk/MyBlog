import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Post, Comment
from blog.token_generator import account_activation_token
from django.test import RequestFactory
from blog.views import RegisterUserView

@pytest.fixture
def user_factory(db):
    def create_user(username = 'TestUser', password = 'TestPassword', email = 'test@mail.ru'):
        if User.objects.filter(username=username).exists():
            return User.objects.filter(username=username).first()
        else:
            user = User.objects.create(username=username, password=password, email=email)
            return user

    return create_user


@pytest.fixture
def comment_factory(db):
    def create_comment(post = None, author = None, text = 'TestText', status = True):
        if Comment.objects.filter(text = text and author == author and post == post).exists():
            return Comment.objects.filter(text = text and author == author and post == post).first()
        else:
            return Comment.objects.create(post = post, author = author, text = text, status = status)

    return create_comment


@pytest.fixture
def post_factory(db):
    def create_post(author = None, text = 'TestText', title = 'Test'):
        if Post.objects.filter(text = text and author == author).exists():
            return Post.objects.filter(text = text and author == author).first()
        else:
            return Post.objects.create(author = author, text = text, title = title)

    return create_post


def test_user_data(db, user_factory):
    user = user_factory(username='hi', password='hi', email='test@mail.ru')
    assert user.username == 'hi' and user.password == 'hi' and user.email == 'test@mail.ru'


def test_default_user_data(db, user_factory):
    user = user_factory(password='hi', email='test@mail.ru')
    assert user.username == 'TestUser' and user.password == 'hi' and user.email == 'test@mail.ru'


def test_is_active_user(db, user_factory):
    user = user_factory()
    assert user.is_active == True


def test_user_created(db, user_factory):
    user = user_factory()
    assert User.objects.filter(username=user.username).exists() == True


def test_post_text(db, user_factory, post_factory):
    user = user_factory()
    post = post_factory(author = user, text = 'TestPost')

    assert post.text == 'TestPost'


def test_post_author(db, user_factory, post_factory):
    user = user_factory()
    post = post_factory(author=user, text='TestPost')

    assert post.author is not None


def test_post_image(db, user_factory, post_factory):
    user = user_factory()
    post = post_factory(author=user, text='TestPost')

    assert post.image is None


def test_post_title(db, user_factory, post_factory):
    user = user_factory()
    post = post_factory(author=user, text='TestPost', title='TestTitle')

    assert post.title == 'TestTitle'


def test_post_str(db, user_factory, post_factory):
    user = user_factory()
    post = post_factory(author=user, text='TestPost', title='some title')

    assert str(post) == post.title


def test_comment_text(db, user_factory, comment_factory, post_factory):
    user = user_factory(username = 'test')
    post = post_factory(author = user)
    comment = comment_factory(post = post, author = user, text = 'hello')

    assert comment.text == 'hello'


def test_comment_author(db, user_factory, comment_factory, post_factory):
    user = user_factory(username = 'test')
    post = post_factory(author = user)
    comment = comment_factory(post = post,  text = 'hello')

    assert comment.author is None


def test_comment_post(db, user_factory, comment_factory, post_factory):
    user = user_factory(username = 'test')
    post = post_factory(author = user)
    comment = comment_factory(post = post, author = user, text = 'hello')

    assert comment.post == post


def test_comment_str(db, user_factory, comment_factory, post_factory):
    user = user_factory(username = 'test')
    post = post_factory(author = user)
    comment = comment_factory(post = post, author = user, text = 'hello')

    assert str(comment) == comment.text


def test_token(db, user_factory):
    user = user_factory()
    token = account_activation_token.make_token(user)
    assert isinstance(token, str) == True and len(token) > 0


def test_register_view(db, user_factory):
    user = user_factory()

    path = reverse('register_page')
    request = RequestFactory().get(path)
    request.user = user
    RegisterUserView(request)
    assert user.is_active == True

