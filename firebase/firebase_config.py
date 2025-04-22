import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the app only once
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'planit-c1d78',  # 👈 Replace with your actual Firebase project ID
    })

# Expose Firestore DB client
db = firestore.client()
