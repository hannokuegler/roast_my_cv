# Quantitative Investing with FinBERT, BERT and DistilRoBERTa

Authors: Aleksandar Gradev, Aleksandar Milosavljevic, Jonatan Acho
Date: 24/11/2025

---

## 1. Project Overview

**Goal:**  
Use large language models (LLMs) to map financial news to sentiment labels and test whether this information can be used to construct profitable trading strategies.

**Main steps:**

1. Download and preprocess labeled financial news
2. Rebalance the dataset to reduce label skew
3. Split data into train / validation / test sets
4. Fine-tune three transformer models for sentiment:
   - **BERT** (general-purpose baseline)
   - **FinBERT** (finance-specific)
   - **DistilRoBERTa** (smaller, faster)
5. Evaluate all models with **macro-averaged F1** and accuracy
6. Use the best model to classify out-of-sample news
7. Aggregate daily sentiment by ticker and map it into **portfolio weights**
8. Backtest long-only and long/short strategies on a universe of stocks

---

## 2. Models and Metrics

### Models

- **BERT**: Generic language model used as a strong baseline
- **FinBERT**: Pretrained on financial text; initial head not aligned with our labels, so we finetune it
- **DistilRoBERTa**: A distilled, faster model; useful when latency or compute is constrained

All models are loaded and fine-tuned via the Hugging Face `transformers` library

### Evaluation

We use:

- **Accuracy**
- **Macro-averaged precision, recall and F1**

Macro F1 is the main selection metric, because it treats negative, neutral and positive classes equally even when the dataset is imbalanced

---

## 3. Data

### Labeled sentiment dataset

- Manually labeled financial news from multiple public sources
- Standardized sentiment labels:
  - `0` = negative  
  - `1` = neutral  
  - `2` = positive  
- We perform class rebalancing to mitigate skewness (undersampling majority classes)
- Final split:
  - **Train**: 70%  
  - **Validation**: 15%  
  - **Test**: 15%

The main notebook handles loading a pre-combined CSV or rebuilding the dataset from individual source files.

### Price data for backtesting

- Daily close prices for all tickers in the selected universe
- Loaded either from a pre-saved CSV (`loadData = True`) or external data sources (Yahoo Finance) via helper functions

---

## 4. Trading Strategy

We transform model predictions into trading signals as follows:

1. Each news article is classified into {negative, neutral, positive} by the selected model

2. For each (date, ticker) pair we aggregate sentiment (average label) across all news items

3. **Long-only strategy**:  
     - Go long on tickers with sufficiently positive average sentiment (avg_label ≥ 1.5)  
     - Allocate equal weights among selected tickers for that day

4. **Long/short strategy**:  
     - Go long on strongly positive tickers (avg_label ≥ 1.5)  
     - Go short on strongly negative tickers (avg_label < 0.5)
     - Weights are scaled to ensure the portfolio is properly normalized

4. Backtest and compare performance (returns, volatility, Sharpe, drawdowns, etc.) against the simple benchmark

---

## 5. Repository Structure

The structure for this project is:

├── project_notebook.ipynb
├── training_notebook.ipynb 
├── data_preprocessing_notebook.ipynb 
├── data/                      
│   ├── prices_DOW_2025-06-01_2025-11-21.csv
│   └── dow_news_all_data.csv
│   └── balanced_sentiment_data_small.csv
│   └── all_data.csv
│   └── SEntFiN-v1.1.csv
│   └── stock_news.csv
├── helpers/                   
│   ├── helperFunction.py
└── README.md                   

## 6. Drive folder

Url to the Google Drive folder, storing the finetuned models:

https://drive.google.com/drive/folders/1RJYVp87S7r1r-Q5iX05HWz9SJofzmAwe?usp=drive_link