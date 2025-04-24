import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the app with the service account key
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\ZisandaNodali\\Documents\\GitHub\\PlanIt\\firebase\\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Expose Firestore DB client
db = firestore.client()

