from firebase.firebase_config import db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    users_ref = db.collection("users")
    hashed_pw = hash_password(password)

    matching_users = users_ref.where("email", "==", email).where("password", "==", hashed_pw).stream()

    for user in matching_users:
        print(f"✅ Welcome back, {user.to_dict()['username']}!")
        return True

    print("❌ Invalid email or password.")
    return False
