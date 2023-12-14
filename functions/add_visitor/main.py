from google.cloud import firestore
import functions_framework
from flask import jsonify

@functions_framework.http
def add_visitor(request):
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204, headers

    request_data = request.get_json()
    cookie = request_data.get('cookie')
    fingerprint = request_data.get('fingerprint')

    db = firestore.Client()
    visitors_ref = db.collection('visitors')

    visitors_ref.add({
        'cookie': cookie,
        'fingerprint': fingerprint,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

    return jsonify({'status': 'success'}), 200, headers