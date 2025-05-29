from lib.db.connection import get_connection

class Author:
    all = {}
    def __init__(self, name, id = None):
        self.name = name
        self.id = id


    @property 
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    def save(self):
        sql = """
        INSERT INTO authors (name) 
        VALUES (?)
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (self.name,))
        self.id = cursor.lastrowid

        Author.all[self.id] = self
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT * FROM authors 
        where id = ?
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return cls(name=row[1], id=row[0])
        else:
            raise Exception("Author not found with id of {id}")
        
    @classmethod
    def find_by_name(cls, name):
        sql = """
        SELECT * FROM authors 
        where name = ?
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (name,))
        row = cursor.fetchone()

        if row:
            return cls(name=row[1], id=row[0])
        else:
            return "Author not found"
        
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql ="""
        SELECT * FROM articles
        WHERE author_id = ?
        """
        cursor.execute(sql, (self.id,))
        return cursor.fetchall()

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql ="""
        SELECT DISTINCT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        return cursor.fetchall()
    
    def add_article(self, magazine, title, cursor):
        sql = """
        INSERT INTO articles (title, magazine_id, author_id)
        VALUES (?, ?, ?)
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql, (title, magazine['id'], self.id))

    def topic_areas(self, cursor):
        sql = """
        SELECT DISTINCT m.category
        FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?
        """

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]


    @classmethod
    def most_articles(cls):
        """Find the author who has written the most articles using SQL query."""
    
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = """
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count
            FROM authors
            LEFT JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id, authors.name
            ORDER BY article_count DESC
            LIMIT 1
        """
        
        cursor.execute(sql)
        row = cursor.fetchone()
        
        conn.close()
        
        if row:   
            article_count = row[2]
            return cls.find_by_name(name=row[1])
        
        return None
    

if __name__ == "__main__":
    from lib.models.article import Article
    from lib.models.magazine import Magazine

    a1 = Author("Jane"); a1.save()
    a2 = Author("John"); a2.save()
    mag = Magazine("World Today", "News"); mag.save()

    Article("News 1", a1.id, mag.id).save()
    Article("News 2", a1.id, mag.id).save()
    Article("Opinion", a2.id, mag.id).save()

    top_author = Author.most_articles()