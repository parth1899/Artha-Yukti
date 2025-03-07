# 📈 Financial Sentiment & Stock Prediction Model  

This project integrates **FinBERT-based sentiment analysis** with an **LSTM-based stock price prediction model** to provide a **comprehensive market analysis**. It dynamically assigns weightage to sentiment and price forecasts to improve investment decision-making.

---

## 🚨 Problem Statement  

📉 **Investors face an overwhelming volume of real-time data, leading to delayed decisions and missed opportunities.**  
❌ **Extracting accurate sentiment from unstructured sources is complex and error-prone, posing high-stakes risks.**  

---

## 🛠️ Solution Approach  

✅ **Custom Nifty50 database (2014–2025, 129,377 rows)** → Cleaned & preprocessed for time-series forecasting.  
✅ **FinBERT-based Sentiment Extraction** → Trained on **1.4M financial headlines** to extract **bullish, bearish, or neutral** sentiment.  
✅ **LSTM-based Time-Series Prediction** → Forecasts stock price trends based on historical market data.  
✅ **User-Friendly Dashboard** → Displays **prediction charts, source citations, analytics, and investment recommendations**.  

---

## 🏗️ System Architecture  

---![architecture](https://github.com/user-attachments/assets/2823d90f-25d0-42c4-9978-02f039406e53)




1️⃣ **Data Acquisition & Reliability**  
   - Customizable ETL from `yfinance` for accurate real-time data.  
   - Fully documented & version-controlled codebase on GitHub.  

2️⃣ **NLP & Sentiment Analysis**  
   - **Structured LLMs** for multi-language financial news processing.  
   - Sentiment classification (**bearish, bullish, neutral**) via **FinBERT**.  

3️⃣ **Forecasting & Dynamic Analysis**  
   - LSTM-based stock price forecasting.  
   - Weighted analysis combining sentiment & confidence scores using a custom formula.  
   - Provides **actionable insights** for investors.  

4️⃣ **Real-Time Processing & Scalability**  
   - Low latency real-time input processing.  
   - Extensive **Flask endpoints** for API-driven predictions.  
   - Cache-based state management for multi-user support.  

5️⃣ **Visualization & User Empowerment**  
   - Multiple interactive **graph view options**.  
   - **Source verification** for user confidence & validation.  

---

## 🎥 Demo  

🔗 *Click the image to watch the demo video!*  

---

## 🚀 Features  

✅ **LSTM & FinBERT Integration** – Combines deep learning & NLP for robust stock forecasting.  
✅ **Sentiment Analysis from Financial News** – Extracts real-time news sentiment.  
✅ **Custom Dynamic Weight Assignment** – Adjusts importance of sentiment vs. prediction confidence.  
✅ **Real-Time Market Predictions** – Generates **buy/hold/sell** signals.  
✅ **Market Analysis Dashboard** – Displays **real-time sentiment, trend predictions, and historical analysis**.  
✅ **Multi-Market Adaptability** – Can be extended to **crypto, forex, and commodities**.  
✅ **Research & Analytics Tool** – Useful for **financial researchers & institutions**.  

---

## ⚙️ Installation  

```bash
# Clone the repository
git clone https://github.com/your-username/financial-sentiment-stock-prediction.git
cd financial-sentiment-stock-prediction

# Install dependencies
pip install -r requirements.txt
