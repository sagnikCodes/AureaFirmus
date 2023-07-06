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
    page_title="📈Closing Price"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


col1,col2=st.columns(2)

with col1:
    stocks=load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_dwivte2j.json")
    st_lottie(stocks)

with col2:
    stocks=load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_fgba6oco.json")
    st_lottie(stocks)


st.title('Predict Stock Price of any Company')
st.write('You can now know the closing price of any Company on the next day! You are just 1 click away!')
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

if(st.button('Predict Closing Price')):
    for layer in gru_model.layers:
      layer.trainable=False
    predicted_price=predict()
    st.write('The expected Closing Price tommorow is '+str(round(predicted_price,2)))
