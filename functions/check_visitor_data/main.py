from google.cloud import firestore
import functions_framework
from flask import jsonify

@functions_framework.http
def check_visitor(request):
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
    unique_id = request_data.get('uniqueId')
    fingerprint = request_data.get('fingerprint')

    db = firestore.Client()
    visitors_ref = db.collection('visitors')
    
    # Check by uniqueId
    if unique_id:
        unique_id_query = visitors_ref.where('cookie', '==', unique_id).limit(1).get()
        if unique_id_query:
            return jsonify({'exists': True, 'cookie': unique_id}), 200, headers

    # Check by fingerprint
    if fingerprint:
        fingerprint_query = visitors_ref.where('fingerprint', '==', fingerprint).limit(1).get()
        if fingerprint_query:
            return jsonify({'exists': True, 'cookie': fingerprint_query[0].to_dict().get('cookie')}), 200, headers

    # Visitor does not exist
    return jsonify({'exists': False}), 200, headers