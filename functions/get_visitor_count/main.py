from google.cloud import firestore
import functions_framework
from flask import jsonify

ALLOWED_ORIGIN = "https://jschluesche.com"

@functions_framework.http
def get_visitor_count(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
        'Access-Control-Allow-Origin': ALLOWED_ORIGIN,
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    origin = request.headers.get('Origin')
    
    if origin != ALLOWED_ORIGIN:
        return jsonify({'error': 'Unauthorized'}), 403, headers

    db = firestore.Client()
    collection_name = 'counters'
    document_name = 'visitorCount'

    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()

    if doc.exists:
        counter_value = doc.to_dict().get('count', 'Counter field not found')
        # Use jsonify to format the response
        return jsonify({'counter_value': counter_value}), 200, headers
    else:
        return jsonify({'error': 'Document not found'}), 404, headers
