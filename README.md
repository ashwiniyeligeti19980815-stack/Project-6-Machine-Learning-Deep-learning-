# Rossmann Sales Forecasting

This project forecasts daily sales for Rossmann stores, merges historical sales and store metadata, and provides a lightweight deployment dashboard.

## Project files
- Notebook: [Rossmann_Sales_Forecasting_Final.ipynb](Rossmann_Sales_Forecasting_Final.ipynb)
- App: [app.py](app.py)
- Dashboard template: [templates/index.html](templates/index.html)
- Blog PDF: [submission/Rossmann_Blog.pdf](submission/Rossmann_Blog.pdf)

## Deployment

The app is configured for Streamlit-compatible hosts and Render's free web service.

- Heroku command: `streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT`
- Render configuration: [render.yaml](render.yaml)

Heroku discontinued new free dynos, so Render is the free-hosting option for this project. To publish it, connect this repository in Render and create a new Web Service using the included `render.yaml`.

## Run locally
```bash
streamlit run app.py
```
Then open the URL shown by Streamlit, usually http://localhost:8501.

## Highlights
- Forecasting baseline using non-linear machine learning
- Feature engineering for promotions, holidays, competition, and seasonal effects
- Flask deployment for prediction and 42-day forecast endpoints
- Deep learning direction using LSTM-style sequence modeling described in the notebook
