import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from helper.query_processing import QueryProcessor
from api_endpoints.news_api import fetch_news
from sentiment_analysis.sentiment import analyze_sentiment
from helper.citations import main
from helper.recommendation_web_scraper import recommend
from helper.predictor import predict_main
import plotly.graph_objects as go
import pandas as pd
from weighted_response.weighted import weighted_main
from api_endpoints.summary import get_insights_from_groq
import json
import base64
import numpy as np
from helper.session_manager import SessionManager

app = Flask(__name__)
CORS(app)

# Global session manager instance
session_manager = SessionManager()

@app.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query not provided"}), 400

    # Check if a session_id is provided; if not, create a new session.
    session_id = data.get("session_id")
    if not session_id or session_manager.get_session(session_id) is None:
        session_id = session_manager.create_session()
    else:
        # Reset the session for a new query.
        session_manager.reset_session(session_id)

    print(session_id)
    session = session_manager.get_session(session_id)
    session.user_query = data['query']
    print(f"Received query: {session.user_query}")

    # Process the query to extract components.
    query_processor = QueryProcessor()
    session.extracted = query_processor.process_query(session.user_query)
    print(f"Extracted components: {session.extracted}")

    session.stock = session.extracted.stock
    print(f"Extracted news tag: {session.extracted.news}")

    return jsonify({"result": "Query processed successfully.", "session_id": session_id})

@app.route('/query_concurrent', methods=['GET'])
def process_query_concurrent():
    session_id = request.args.get("session_id")
    session = session_manager.get_session(session_id)
    if not session:
        return jsonify({"error": "No session found. Please call /query first."}), 400

    print(f"Extracted components: {session.extracted}")

    # Call the helper function sequentially.
    try:
        news_result = fetch_news(session.extracted.news)
        results = {"news": news_result}
    except Exception as exc:
        results = {"news": {"error": str(exc)}}

    # Extract news content for sentiment analysis.
    news_articles = results.get("news", {}).get("articles", [])
    if news_articles and "content" in news_articles[0]:
        session.news_analysis = news_articles[0]["content"]
    else:
        session.news_analysis = "No relevant news content available."

    print(f"Stored news_analysis: {session.news_analysis}")
    return jsonify({"result": results})


@app.route('/sentiment', methods=['GET'])
def get_sentiment():
    session_id = request.args.get("session_id")
    session = session_manager.get_session(session_id)
    if not session:
         return jsonify({"error": "No session found. Please call /query first."}), 400

    # print(f"News analysis: {session.news_analysis}")
    sentiment_result = analyze_sentiment(session.news_analysis)
    # Save the sentiment result to the session.
    for item in sentiment_result:
         print(f"Label: {item['label']} | Score: {item['score']:.4f}")
         session.sentiment = item['label']

    return jsonify({"result": sentiment_result})

@app.route('/validations', methods=['GET'])
def get_validations():
    session_id = request.args.get("session_id")
    session = session_manager.get_session(session_id)
    if not session:
         return jsonify({"error": "No session found. Please call /query first."}), 400
    
    if session.citations is None:
        session.citations = main(session.stock)
    # print(f"Citations: {session.citations}")
    return jsonify({"result": session.citations})

@app.route('/graphs', methods=['GET'])
def get_graphs():
    session_id = request.args.get("session_id")
    session = session_manager.get_session(session_id)
    if not session:
         return jsonify({"error": "No session found. Please call /query first."}), 400

    # Generate predictions and save a temporary CSV file.
    predict_main(session.stock, "2025-08-08")
    df = pd.read_csv('temp.csv')

    trace_observed = go.Scatter(
         x=df[df['predicted'] == 0]['Date'],
         y=df[df['predicted'] == 0]['Close'],
         mode='lines+markers',
         name='Observed',
         line=dict(color='blue')
    )
    trace_predicted = go.Scatter(
         x=df[df['predicted'] == 1]['Date'],
         y=df[df['predicted'] == 1]['Close'],
         mode='lines+markers',
         name='Predicted',
         line=dict(color='red')
    )

    fig = go.Figure(data=[trace_observed, trace_predicted])
    fig.update_layout(
         title=f'{session.stock} Close Price',
         xaxis_title='Date',
         yaxis_title='Close Price'
    )
    fig.write_json('chart.json')

    with open("chart.json", "r") as f:
         chart_data = json.load(f)

    # Decode binary data if needed.
    for trace in chart_data.get("data", []):
         y_val = trace.get("y")
         if isinstance(y_val, dict) and "bdata" in y_val:
             bdata = y_val["bdata"]
             dtype = y_val.get("dtype", "f8")
             y_bytes = base64.b64decode(bdata)
             y_array = np.frombuffer(y_bytes, dtype=np.float64)
             trace["y"] = y_array.tolist()

    observed_trace = next((trace for trace in chart_data["data"] if trace.get("name") == "Observed"), None)
    predicted_trace = next((trace for trace in chart_data["data"] if trace.get("name") == "Predicted"), None)

    if observed_trace is None or predicted_trace is None:
         raise ValueError("Could not find both 'Observed' and 'Predicted' traces in the data.")

    obs_last_x = observed_trace["x"][-1]
    obs_last_y = observed_trace["y"][-1]
    pred_first_x = predicted_trace["x"][0]
    pred_first_y = predicted_trace["y"][0]

    join_trace = {
         "x": [obs_last_x, pred_first_x],
         "y": [obs_last_y, pred_first_y],
         "mode": "lines",
         "line": {"color": "green", "dash": "dash"},
         "name": "Join"
    }

    chart_data["data"].append(join_trace)
    fig = go.Figure(data=chart_data["data"], layout=chart_data["layout"])
    html = fig.to_html(full_html=True)
    return html

@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    session_id = request.args.get("session_id")
    session = session_manager.get_session(session_id)
    if not session:
         return jsonify({"error": "No session found. Please call /query first."}), 400

    intermediate_result = recommend(session.stock)
    session.citations = intermediate_result[0]
    print("the citations are: ", session.citations)
    result = intermediate_result[1]
    print(result)
    return jsonify({
         "sentiment": session.sentiment,
         "result": result.dict(by_alias=True)
    })

@app.route('/output_text', methods=['GET'])
def get_output_text():
    session_id = request.args.get("session_id")
    session = session_manager.get_session(session_id)
    if not session:
         return jsonify({"error": "No session found. Please call /query first."}), 400

    target_date = "2025-03-02"
    adjusted_price, weight_distribution = weighted_main(session.stock, target_date, session.news_analysis)
    adjusted_price = round(adjusted_price, 2)
    print("\n🔹 Adjusted Predicted Close Price:", adjusted_price)
    print("🔹 Weight Distribution:", weight_distribution)

    result = get_insights_from_groq(session.user_query, session.sentiment, session.news_analysis,
                                     session.stock, adjusted_price, weight_distribution)
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
