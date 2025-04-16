from firebase.firebase_config import db
from auth.register import register_user
from auth.login import login_user
from ui import auth_gui

def test_firebase_connection():
    doc_ref = db.collection("testCollection").document("testDoc")
    doc_ref.set({
        "message": "Hello from Planit!",
        "status": "connected ✅"
    })
    print("Test document created successfully!")

if __name__ == "__main__":
    test_firebase_connection()

#Code for registering and logging in users   
if __name__ == "__main__":
    print("1. Register")
    print("2. Login")
    choice = input("Select an option: ")

    if choice == "1":
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        register_user(username, email, password)

    elif choice == "2":
        email = input("Enter email: ")
        password = input("Enter password: ")
        login_user(email, password)

    else:
        print("❌ Invalid choice.")