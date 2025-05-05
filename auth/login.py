from firebase.firebase_config import db
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import auth
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    try:
        users_ref = db.collection("users")
        hashed_pw = hash_password(password)

        # Step 1: Find user in Firestore
        matching_users = users_ref.where(filter=FieldFilter("email", "==", email))\
                                  .where(filter=FieldFilter("password", "==", hashed_pw))\
                                  .stream()

        for user in matching_users:
            user_data = user.to_dict()
            user_data['id'] = user.id

            # Step 2: Fetch user from Firebase Auth and check verification
            firebase_user = auth.get_user_by_email(email)

            if not firebase_user.email_verified:
                print("⚠️ Email not verified. Please check your inbox.")
                return "unverified"

            print(f"✅ Welcome back, {user_data['username']}!")
            return user_data

        print("❌ Invalid email or password.")
        return None

    except Exception as e:
        print(f"❌ Login error: {e}")
        return None
