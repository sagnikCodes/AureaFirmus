import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import datetime
import time
import yfinance as yf
import pickle
import tensorflow as tf
from streamlit_lottie import st_lottie
import requests



st.set_page_config(
    page_title="📈Opening Price"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    
stocks=load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_F3v2Nj.json")
st_lottie(stocks,width=250,height=300)

st.title('Predict Stock Price of any Company')
st.write("Discover the anticipated range of tomorrow's opening price for any company with just a single click, providing you with valuable insights.")
st.write('Disclaimer : The Prediction might take upto a minute. Please be patient')
scaler=joblib.load('scaler.pkl')
gru_model=tf.keras.models.load_model('gru_model.h5')

def inverse(a,b):
  m1=b.min()
  m2=b.max()
  return a*(m2-m1)+m1

companyDict=joblib.load('company')
company_name=st.selectbox("Select Company",list(companyDict.keys()))
company_ticker=companyDict[company_name]

def predict():
    #Extracting the data of the company entered by user 
    ticker_symbol=company_ticker.upper()+".NS"
    days_back=15
    interval='15m'
    end_date=datetime.datetime.now().strftime('%Y-%m-%d')
    start_date=(datetime.datetime.now()-datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
    company_data=yf.download(ticker_symbol,start=start_date,end=end_date,interval=interval)['Close']
    df=scaler.fit_transform(np.array(company_data).reshape(-1,1))
    new_data=pd.DataFrame()
    df=np.array(df)
    l=[]
    for i in range(df.shape[0]):
        l.append(df[i][0])
    new_data['Close']=l
    new_data=pd.DataFrame(new_data,columns=["Close"])
    def create_dataset(X, y, time_steps=1):
        Xs,ys=[],[]
        for i in range(len(X)-time_steps):
            Xs.append(X.iloc[i:(i+time_steps)].values)
            ys.append(y.iloc[i+time_steps])
        return np.array(Xs),np.array(ys)
    X_test,y_test=create_dataset(new_data[['Close']], new_data[['Close']],60)

    #Fine tuning the overall model trained
    gru_model.fit(X_test,y_test,epochs=3,batch_size=8)

    new_x_test=np.array(new_data[len(company_data)-60:]).reshape(1,60,1)
    pred=gru_model.predict(new_x_test)
    next_predicted=inverse(pred,company_data)[0][0]
    return next_predicted

if(st.button('Predict Range')):
    predicted_arr=[]
    for layer in gru_model.layers:
        layer.trainable=False
    for i in range(2):
        predicted_price=predict()
        predicted_arr.append(predicted_price)
    predicted_price=np.array(predicted_price)
    mean=predicted_price.mean()
    standard_deviation=predicted_price.std()+0.5643
    st.write(f'The Opening Price can lie somewhere between {round(mean-standard_deviation,3)} and {round(mean+standard_deviation,3)}')
