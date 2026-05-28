import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase solo una vez
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Cliente Firestore
db = firestore.client()