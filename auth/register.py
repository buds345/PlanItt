from firebase.firebase_config import db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    users_ref = db.collection("users")
    existing_users = users_ref.where("email", "==", email).stream()

    if any(existing_users):
        print("❌ Email already registered.")
        return False

    user_data = {
        "username": username,
        "email": email,
        "password": hash_password(password)
    }

    users_ref.add(user_data)
    print("✅ User registered successfully.")
    return True
