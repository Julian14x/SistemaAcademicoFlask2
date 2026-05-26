import os
import json
import firebase_admin
from firebase_admin import credentials

# Carga las credenciales desde la variable de entorno de Vercel
cred_json = json.loads(os.environ.get('FIREBASE_CREDENCIAL'))
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

