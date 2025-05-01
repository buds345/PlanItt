from firebase.firebase_config import db
from google.cloud.firestore_v1.base_query import FieldFilter
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    users_ref = db.collection("users")
    hashed_pw = hash_password(password)

    matching_users = users_ref.where(filter=FieldFilter("email", "==", email)).where(
    filter=FieldFilter("password", "==", hashed_pw)
    ).stream()


    for user in matching_users:
        user_data = user.to_dict()
        user_data['id'] = user.id  # Save Firestore document ID if needed
        print(f"✅ Welcome back, {user_data['username']}!")
        return user_data  # Return user data instead of just True

    print("❌ Invalid email or password.")
    return None

