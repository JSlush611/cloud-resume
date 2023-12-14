from google.cloud import firestore
import functions_framework
from flask import jsonify

@functions_framework.http
def increment_visitor_count(request):
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204, headers

    db = firestore.Client()
    counters_ref = db.collection('counters')
    visitor_count_doc = counters_ref.document('visitorCount')

    # Transaction to increment visitor count and retrieve new count
    @firestore.transactional
    def update_counter(transaction, doc_ref):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists:
            current_count = snapshot.get('count')
            new_count = current_count + 1
            transaction.update(doc_ref, {
                'count': new_count
            })
            return new_count
        else:
            # Handling case where the document might not exist
            transaction.set(doc_ref, {'count': 1})
            return 1

    transaction = db.transaction()
    updated_count = update_counter(transaction, visitor_count_doc)

    return jsonify({'updated_count': updated_count}), 200, headers