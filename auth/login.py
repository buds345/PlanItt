from firebase.firebase_config import db
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import auth
import hashlib
import tkinter.messagebox as messagebox
import re
import webbrowser

def clean_header_value(value):
    # Remove newlines and carriage returns from header values (for security and email compliance)
    return re.sub(r'[\r\n]', '', value.strip())
    
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
def send_password_reset(email):
    if not email:
        messagebox.showerror("Missing Email", "Please enter your email address.")
        return

    try:
        # Confirm the user exists in Firebase
        auth.get_user_by_email(email)

        # Generate reset link
        reset_link = auth.generate_password_reset_link(email)

        # Open the reset link in user's default browser
        webbrowser.open(reset_link)

        # Show success message
        messagebox.showinfo("Reset Link Sent", "A reset link has been opened in your browser.\nYou can reset your password there.")

    except auth.UserNotFoundError:
        messagebox.showerror("Error", "Email not found in Firebase.")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating reset link:\n{e}")
