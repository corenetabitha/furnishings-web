from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    all = {}
    def __init__(self, title, author_id, magazine_id, id = None):
        author = Author.find_by_id(author_id)
        if not author:
            raise Exception("Put in valid author id")
        mag = Magazine.find_by_id(magazine_id)  
        if not mag:
            raise Exception("Put in valid magazine id")

        self.title = title
        self.magazine_id = magazine_id
        self.author_id = author_id
        self.id = id

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not len(value) > 3:
            raise ValueError("Title must be more than 3 characters.")
        self._title = value
        
    def save(self):
        sql = """
        INSERT INTO articles (title, author_id, magazine_id)
        VALUES (?, ?, ?)
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql,(self.title, self.author_id, self.magazine_id,))
        self.id = cursor.lastrowid

        Article.all[self.id] = self
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        sql ="""
        SELECT * from articles
        WHERE id = ?
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql,(id,))
        row = cursor.fetchone()

        if row:
            return Article(title=row[1], author_id=row[2],magazine_id=row[3])
        else:
            raise Exception(f"Article with ID:{id} not found")
        
    @classmethod
    def find_by_title(cls, title):
        sql ="""
        SELECT * from articles
        WHERE title = ?
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql,(title,))
        row = cursor.fetchone()

        if row:
            return Article(title=row[1], author_id=row[2],magazine_id=row[3])
        else:
            raise Exception(f"Article with Title:{title} not found")
        
    @classmethod
    def find_by_author(cls, author_id):
        sql ="""
        SELECT * from articles
        WHERE author_id = ?
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql,(author_id,))
        row = cursor.fetchone()

        if row:
            return Article(title=row[1], author_id=row[2],magazine_id=row[3])
        else:
            raise Exception(f"Article with Author ID:{author_id} not found")    