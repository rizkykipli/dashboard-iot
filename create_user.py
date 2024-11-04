from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Meminta input dari pengguna
username = input("Enter username: ")
password = input("Enter password: ")

# Menggunakan app context untuk mengakses database
with app.app_context():
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print(f"User '{username}' created!")

