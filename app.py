from flask import Flask, request, jsonify
from flask_cors import CORS
from helper.query_processing import QueryProcessor
from api_endpoints.stock_api import fetch_stock
from api_endpoints.news_api import fetch_news
from api_endpoints.twitter_api import fetch_twitter
from sentiment_analysis.sentiment import analyze_sentiment
from concurrent.futures import ThreadPoolExecutor, as_completed
from helper.citations import main
from helper.recommendation_web_scraper import recommend
from helper.predictor import predict_main
import plotly.graph_objects as go
import pandas as pd
from weighted_response.weighted import weighted_main
from api_endpoints.summary import get_insights_from_groq
import json
import base64
import plotly.graph_objects as go
import numpy as np

app = Flask(__name__)
CORS(app)

# Global variable to hold the extracted query components.
extracted = None
user_query = None
news_analysis = None # global variable to pass news data to sentiment analysis
stock = None
sentiment = None
news_data = None
citations = None

@app.route('/query', methods=['POST'])
def process_query():

    global extracted, user_query, news_analysis, stock, sentiment, news_data

    # Reset all global variables at the start of each request
    extracted = None
    user_query = None
    news_analysis = None
    stock = None
    sentiment = None
    news_data = None

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query not provided"}), 400

    user_query = data['query']
    print(f"Received query: {user_query}")

    # Process the query to extract components.
    query_processor = QueryProcessor()
    extracted = query_processor.process_query(user_query)
    print(f"Extracted components: {extracted}")

    print(f"Extracted news tag: {extracted.news}")

    stock = extracted.stock

    # Store the extracted components in a global variable.
    # global extracted
    # extracted = extracted

    # return jsonify({"result": extracted.dict()})
    return jsonify({"result": "Query processed successfully."})

@app.route('/query_concurrent', methods=['GET'])
def process_query_concurrent():
    # Ensure that the global_extracted has been set.
    global extracted
    if not extracted:
        return jsonify({"error": "No extracted data found. Please call /query first."}), 400
    
    print(f"Extracted components: {extracted}")

    # Call the three helper functions concurrently using the global extracted components.
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_component = {
            executor.submit(fetch_news, extracted.news): "news",
            # executor.submit(fetch_stock, extracted.stock): "stock",
            # executor.submit(fetch_twitter, extracted.twitter): "twitter"
        }
        results = {}
        for future in as_completed(future_to_component):
            component = future_to_component[future]
            try:
                results[component] = future.result()
            except Exception as exc:
                results[component] = {"error": str(exc)}

    global news_analysis
    # Extract content from the first article
    news_articles = results.get("news", {}).get("articles", [])
    if news_articles and "content" in news_articles[0]:
        news_analysis = news_articles[0]["content"]
    else:
        news_analysis = "No relevant news content available."

    print(f"Stored news_analysis: {news_analysis}")

    return jsonify({"result": results})

@app.route('/sentiment', methods=['GET'])
def get_sentiment():
    global news_analysis
    print(f"News analysis: {news_analysis}")
    sentiment_result = analyze_sentiment(news_analysis)

    global sentiment
    for item in sentiment_result:
        print(f"Label: {item['label']} | Score: {item['score']:.4f}")
        sentiment = item['label']

    return jsonify({"result": sentiment_result})

@app.route('/validations', methods=['GET'])
def get_validations():
    # global extracted
    # print(f"Stock name: {extracted.stock}")
    # citations = main(extracted.stock)
    global stock
    global citations
    citations = main(stock)
    # print(f"Citations: {citations}")
    # print("Stock name : ADANIPORTS")
    # citations = main("ADANIPORTS")
    print(f"Citations: {citations}")
    return jsonify({"result": citations})

@app.route('/graphs', methods=['GET'])
def get_graphs():
    global stock
    # print(f"Stock name: {extracted.stock}")
    # stock_name = "ADANIPORTS"
    predict_main(stock, "2025-08-08") # creates a temp.csv

    # Read the CSV file
    df = pd.read_csv('temp.csv')

    # Create two traces:
    #  - One for observed (predicted == 0) values, colored blue
    #  - One for predicted (predicted == 1) values, colored red
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
        title='Stock Close Price',
        xaxis_title='Date',
        yaxis_title='Close Price'
    )

    # return jsonify(fig)
    # Save the JSON spec to a file or return it in a response.
    fig.write_json('chart.json')

    # Load the JSON file (ensure chart.json is in the same directory or adjust the path)
    with open("chart.json", "r") as f:
        chart_data = json.load(f)

    # Decode the binary data for y-values in each trace, if needed.
    for trace in chart_data.get("data", []):
        y_val = trace.get("y")
        if isinstance(y_val, dict) and "bdata" in y_val:
            # Get the base64 encoded binary data and decode it into a numpy array.
            bdata = y_val["bdata"]
            dtype = y_val.get("dtype", "f8")
            # Decode base64 bytes and convert to a numpy array.
            y_bytes = base64.b64decode(bdata)
            y_array = np.frombuffer(y_bytes, dtype=np.float64)
            # Replace the "y" value with a standard Python list.
            trace["y"] = y_array.tolist()

    # Identify the Observed and Predicted traces by name.
    observed_trace = next((trace for trace in chart_data["data"] if trace.get("name") == "Observed"), None)
    predicted_trace = next((trace for trace in chart_data["data"] if trace.get("name") == "Predicted"), None)

    if observed_trace is None or predicted_trace is None:
        raise ValueError("Could not find both 'Observed' and 'Predicted' traces in the data.")

    # Get the last point from Observed and the first point from Predicted.
    obs_last_x = observed_trace["x"][-1]
    obs_last_y = observed_trace["y"][-1]
    pred_first_x = predicted_trace["x"][0]
    pred_first_y = predicted_trace["y"][0]

    # Create a new trace that joins these two points.
    join_trace = {
        "x": [obs_last_x, pred_first_x],
        "y": [obs_last_y, pred_first_y],
        "mode": "lines",
        "line": {"color": "green", "dash": "dash"},
        "name": "Join"
    }

    # Append the join trace to the chart data.
    chart_data["data"].append(join_trace)

    # Create the Plotly figure with the updated data and layout.
    fig = go.Figure(data=chart_data["data"], layout=chart_data["layout"])

    # Generate the full HTML and return it.
    html = fig.to_html(full_html=True)
    return html


    return jsonify({"result": "Graphs will be displayed here."})

@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    # global user_query
    # print(f"User query: {user_query}")
    # stock_name = "ADANIPORTS"
    global stock
    global citations
    result = recommend(stock)
    global sentiment
    return jsonify({
        "sentiment": sentiment,
        "result": result.dict(by_alias=True)
    })
    # return jsonify({"result": "Recommendation will be displayed here."})

@app.route('/output_text', methods=['GET'])
def get_output_text():

    global stock
    target_date = "2025-03-02"
    global news_analysis
    global sentiment
    global user_query

    adjusted_price, weight_distribution = weighted_main(stock, target_date, news_analysis)

    adjusted_price = round(adjusted_price, 2)

    print("\n🔹 Adjusted Predicted Close Price:", adjusted_price)
    print("🔹 Weight Distribution:", weight_distribution)

    result = get_insights_from_groq(user_query, sentiment, news_analysis, stock, adjusted_price, weight_distribution)

    print(result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
