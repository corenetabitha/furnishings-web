import pytest
from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def setup_function():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    conn.close()

def test_create_article():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    article = Article("My Story", author.id, mag.id)
    article.save()
    assert article.id is not None

def test_find_by_id():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    article = Article("Test Article", author.id, mag.id)
    article.save()
    found = Article.find_by_id(article.id)
    assert found.title ==  "Test Article"

def test_find_by_title():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    article = Article("Test Article", author.id, mag.id)
    article.save()
    found = Article.find_by_title(article.title)
    assert found.title == "Test Article"

def test_find_by_author():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    article = Article("Test Article", author.id, mag.id)
    article.save()
    found = Article.find_by_author(author.id)
    assert found.title == "Test Article"

def test_valid_name_setter():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    article = Article("Initial Name", author.id, mag.id)
    article.save()
    article.title = "Updated Name"
    assert article.title == "Updated Name"

def test_invalid_name_type():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    with pytest.raises(TypeError):
        article = Article(123, author.id, mag.id)

def test_invalid_name_length():
    author = Author("Writer")
    author.save()
    mag = Magazine("Cool Mag", "Culture")
    mag.save()
    with pytest.raises(ValueError):
        article = Article("", author.id, mag.id)