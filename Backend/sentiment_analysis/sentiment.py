from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def analyze_sentiment(text: str):
    # Define the model repository name
    model_name = "StephanAkkerman/FinTwitBERT-sentiment"
    
    # Load the tokenizer and model from Hugging Face Hub
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    # Create a sentiment analysis pipeline using the loaded model
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    # Analyze the sentiment of the input text
    result = sentiment_pipeline(text)
    return result

# if _name_ == "_main_":
#     # Prompt the user for a financial tweet or news headline
#     input_text = input("Enter a financial tweet or news headline: ")
    
#     # Get sentiment analysis result
#     analysis_result = analyze_sentiment(input_text)
    
#     # Display the result
#     print("\nSentiment Analysis Result:")
#     for item in analysis_result:
#         print(f"Label: {item['label']} | Score: {item['score']:.4f}")