from flask import Flask, request, jsonify
from helper.query_processing import QueryProcessor
app = Flask(__name__)

# Define a route to handle incoming queries.
@app.route('/query', methods=['POST'])
def process_query():
    # Get JSON data from the request body.
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query not provided"}), 400

    user_query = data['query']
    print(f"Received query: {user_query}")

    query_processor = QueryProcessor()
    extracted = query_processor.process_query(user_query)

    print(f"Extracted components: {extracted}")

    
    # Return the processed result as a JSON response.
    return jsonify({"result": extracted.dict()})

if __name__ == '__main__':
    app.run(debug=True)
