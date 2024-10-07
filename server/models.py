from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))  # Limit to 10 characters
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            print("Validation Error: Author name cannot be empty")
            raise ValueError("Author must have a name")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            print(f"Validation Error: Invalid phone number '{phone_number}'")
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            print(f"Validation Error: Content too short: {len(content)} characters")
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            print(f"Validation Error: Summary too long: {len(summary)} characters")
            raise ValueError("Post summary must be no more than 250 characters")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            print(f"Validation Error: Invalid category '{category}'")
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            print(f"Validation Error: Title not clickbait-y: {title}")
            raise ValueError("Title must be clickbait-y (include 'Won't Believe', 'Secret', 'Top', or 'Guess')")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
