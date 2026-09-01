# Mobile Phone Analytics Dashboard

An interactive data analysis dashboard built using Python, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit.

## Project Overview

This project analyzes mobile phone data to identify trends in pricing, brands, RAM, storage, camera specifications, battery capacity, ratings, and customer reviews.

The project provides an interactive Streamlit dashboard where users can filter the data and explore different aspects of mobile phone specifications and pricing.

## Features

* Interactive brand filtering
* Price range filtering
* RAM filtering
* Storage filtering
* Brand comparison
* Average price analysis
* Price distribution
* Most affordable phones
* Most expensive phones
* RAM vs price analysis
* Storage vs price analysis
* Rating analysis
* Camera vs price analysis
* Battery vs price analysis
* Correlation analysis
* Automated key insights
* Interactive data table

## Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Streamlit

## Project Structure

```text
Mobile_Phone_Analytics/
│
├── app.py
├── mobile_phones.csv
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Hamalesh-SV/mobile-phone-analytics.git
```

### 2. Open the project folder

```bash
cd mobile-phone-analytics
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Analysis Performed

### Brand Analysis

* Number of phones by brand
* Average price by brand
* Brand summary

### Pricing Analysis

* Price distribution
* Minimum price
* Average price
* Median price
* Maximum price
* Affordable phones
* Expensive phones

### Specification Analysis

* RAM vs price
* Storage vs price
* Average price by RAM
* Average price by storage
* RAM-price correlation
* Storage-price correlation

### Rating Analysis

* Rating distribution
* Average rating by brand
* Top-rated phones
* Camera vs price
* Battery vs price

### Correlation Analysis

A correlation heatmap is used to analyze relationships between:

* Price
* RAM
* Storage
* Camera
* Battery
* Rating
* Reviews

## Learning Outcomes

Through this project, I practiced:

* Data cleaning and filtering
* Data aggregation using Pandas
* Statistical calculations using NumPy
* Data visualization using Matplotlib
* Statistical visualization using Seaborn
* Building interactive dashboards using Streamlit
* Git and GitHub version control

## Future Improvements

* Add interactive Plotly charts
* Add mobile phone recommendation functionality
* Add price prediction using Machine Learning
* Add deployment using Streamlit Community Cloud
* Add more real-world mobile phone datasets

## Author

Hamalesh sv
GitHub: https://github.com/Hamalesh-SV
