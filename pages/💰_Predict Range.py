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

st.title('Predict Stock Price of any Company')
st.write('You can now get an idea of what is gonna be the range of  opening price of any company in just a single click.\n\n')

st.write('Disclaimer : The Prediction might take upto a minute. Please be patient')
scaler=joblib.load('scaler.pkl')
gru_model=tf.keras.models.load_model('gru_model.h5')

def inverse(a,b):
  m1=b.min()
  m2=b.max()
  return a*(m2-m1)+m1

company_name=st.text_input("Enter Company Name")

def predict():
    #Extracting the data of the company entered by user 
    ticker_symbol=company_name.upper()+".NS"
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
    gru_model.fit(X_test,y_test,epochs=10,batch_size=8)

    new_x_test=np.array(new_data[len(company_data)-60:]).reshape(1,60,1)
    pred=gru_model.predict(new_x_test)
    next_predicted=inverse(pred,company_data)[0][0]
    return next_predicted

if(st.button('Predict Range')):
    predicted_arr=[]
    for layer in gru_model.layers:
        layer.trainable=False
    for i in range(5):
        predicted_price=predict()
        predicted_arr.append(predicted_price)
    predicted_price=np.array(predicted_price)
    mean=predicted_price.mean()
    standard_deviation=predicted_price.std()+0.5643
    lowerBound=mean-standard_deviation
    upperBound=mean+standard_deviation
    st.write(f'The expected Range of Opening Price for {company_name} tommorow is [ {lowerBound},{upperBound} ]')
