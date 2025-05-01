import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("C:\\Users\\27631\\3D Objects\\PlanIt-3\\firebase\\serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()
