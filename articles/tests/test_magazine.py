import pytest 
from lib.db.connection import get_connection
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.models.author import Author



def setup_function():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    conn.close()

def test_create_magazine():
    mag = Magazine("Test Mag", "Test Category")
    mag.save()
    assert mag.id is not None

def test_find_by_id():
    mag = Magazine("Test Mag", "Test Category")
    mag.save()
    found = Magazine.find_by_id(mag.id)
    assert found.name ==  "Test Mag"

def test_find_by_name():
    mag = Magazine("Test Mag", "Test Category")
    mag.save()
    found = Magazine.find_by_name(mag.name)
    assert found.name ==  "Test Mag"

def test_find_by_category():
    mag = Magazine("Test Mag", "Test Category")
    mag.save()
    found = Magazine.find_by_category(mag.category)
    assert found.category ==  "Test Category"

def test_valid_name_setter():
    mag = Magazine("Initial Name", "Test Category")
    mag.name = "Updated Name"
    assert mag.name == "Updated Name"

def test_invalid_name_type():
    with pytest.raises(TypeError):
        mag = Magazine(123, "Test Cat")  

def test_invalid_name_length():
    with pytest.raises(ValueError):
        mag = Magazine("", "Test Cat") 

def test_valid_category_setter():
    mag = Magazine("Test Name", "Init Category")
    mag.category = "Updated Category"
    assert mag.category == "Updated Category"

def test_invalid_category_type():
    with pytest.raises(TypeError):
        mag = Magazine("Test Name", 123)  

def test_invalid_category_length():
    with pytest.raises(ValueError):
        mag = Magazine("Test Name", "") 

def test_authors_for_magazine():
    author1 = Author("Author One"); author1.save()
    author2 = Author("Author Two"); author2.save()
    mag = Magazine("Tech Monthly", "Technology"); mag.save()
    Article("AI Revolution", author1.id, mag.id).save()
    Article("Cybersecurity", author2.id, mag.id).save()

    authors = mag.contributors()  
    author_names = [author.name for author in authors]

    assert "Author One" in author_names
    assert "Author Two" in author_names
    assert len(authors) == 2

def test_contributing_authors():
    mag1 = Magazine("Culture Weekly", "Culture"); mag1.save()
    mag2 = Magazine("Solo Digest", "Lifestyle"); mag2.save()

    author1 = Author("Alice"); author1.save()
    author2 = Author("Bob"); author2.save()

    Article("Article A", author1.id, mag1.id).save()
    Article("Article B", author2.id, mag1.id).save()
    Article("Solo Piece", author1.id, mag2.id).save()

    magazines = Magazine.contributing_authors_authors()  
    names = [magazine.name for magazine in magazines]
    for mag in magazines:
        print(mag.name, mag.id)

    assert "Culture Weekly" in names
    assert "Solo Digest" not in names

def test_article_count_per_magazine():
    mag = Magazine("Science World", "Science"); mag.save()
    author = Author("Dr. Smith"); author.save()

    Article("Quantum Physics", author.id, mag.id).save()
    Article("Black Holes", author.id, mag.id).save()

    assert mag.article_count() == 2  