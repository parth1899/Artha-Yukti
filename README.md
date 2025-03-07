# 📈 ArthaYukti – A Deep Learning-Driven Financial Sentiment Analysis & Stock Forecasting Platform
Built for INDOvateAI Sprint 2025 | Secured Second Prize 🏆

This project integrates FinBERT-based sentiment analysis with an LSTM-based stock price prediction model to provide a comprehensive market analysis. It dynamically assigns weightage to sentiment and price forecasts to improve investment decision-making.

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

![architecture](https://github.com/user-attachments/assets/bca71941-0f8e-47dd-8680-df9d8223de0a)


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

https://github.com/user-attachments/assets/4c9511a8-e48e-4f45-85fd-0fcb628f0f8a

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

## ⚙️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/parth1899/IndovateAI.git
```

### 2️⃣ Backend Setup  
```bash
cd Backend

# Create and activate a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt

# Running the server
python ./app.py
```

### 3️⃣ Frontend Setup  
```bash
cd ../Frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
