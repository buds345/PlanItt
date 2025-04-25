from firebase.firebase_config import db
from firebase_admin import auth

from firebase.email_utils import send_verification_email


import hashlib


def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    """Register a new user in Firebase Auth and Firestore, and send verification email."""
    try:
        # Check if email is already used in Firestore
        users_ref = db.collection("users")
        existing_users = users_ref.where("email", "==", email).stream()

        if any(existing_users):
            print("❌ Email already registered in Firestore.")
            return False

        # Create user in Firebase Auth
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=username,
        )

        # Store user info in Firestore
        users_ref.add({
            "username": username,
            "email": email,
            "password": hash_password(password),
            "uid": user.uid,
            "is_verified": False
        })

        # Generate email verification link
        verification_link = auth.generate_email_verification_link(email)

        # Send the email via your own utility
        send_verification_email(email, verification_link)

        print("✅ User registered successfully.")
        print("📧 Verification email sent to:", email)
        return True

    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False


# Manual test (only runs when executed directly)
if __name__ == "__main__":
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    register_user(username, email, password)
