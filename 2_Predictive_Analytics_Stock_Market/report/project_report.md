# Predictive Analytics for Stock Market Movements

## 1. Introduction
Stock prices are time-dependent financial observations affected by many factors. This project demonstrates a machine-learning workflow for predicting next-day price direction from historical market data.

## 2. Objective
Predict whether the next trading day's closing price will be higher than the current closing price.

## 3. Dataset
Historical OHLCV data sourced from Yahoo Finance and provided through the assignment's Kaggle dataset options.

## 4. Data Preparation
The workflow converts dates, validates numeric fields, removes duplicate records, sorts chronologically and removes rows without required values.

## 5. Feature Engineering
The baseline model uses:
- One-day return
- 5-day moving average
- 20-day moving average
- 14-period RSI
- Trading volume

## 6. Model
A Logistic Regression classifier is used as a transparent baseline. The data is split chronologically into 80% training and 20% testing data to avoid using future observations to train the model.

## 7. Evaluation
The project calculates:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Run `python/stock_prediction.py` after adding `data/stock.csv` to generate the actual metrics for the selected stock dataset.

## 8. Visualization
The project generates a test-period closing-price chart and exports prediction results for further analysis.

## 9. Limitations and Risk Factors
Stock prices are influenced by news, macroeconomic conditions, company fundamentals, market structure and unexpected events. Technical indicators alone are insufficient to establish reliable future returns. The baseline model is educational and does not include transaction costs, slippage, portfolio construction, risk management or live-market validation.

## 10. Conclusion
The project demonstrates the complete predictive analytics lifecycle: historical data preparation, feature engineering, chronological model validation, classification, evaluation and documentation of limitations.

**Disclaimer:** This project is for educational purposes only and is not financial or investment advice.
