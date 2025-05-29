from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Seed authors
a1 = Author("Alice")
a1.save()
a2 = Author("Bob")
a2.save()

# Seed magazines
m1 = Magazine("Science Weekly", "Science")
m1.save()
m2 = Magazine("Tech Monthly", "Technology")
m2.save()

# Seed articles
Article("Quantum Theory", a1.id, m1.id).save()
Article("AI Advances", a1.id, m2.id).save()
Article("Neural Networks", a2.id, m2.id).save()