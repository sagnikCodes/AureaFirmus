import pandas as pd
# import pickle
# import numpy as np
# import matplotlib.pyplot as plt
# import datetime
# import time
# import yfinance as yf
# from sklearn.preprocessing import MinMaxScaler
# def inverse(a,b):
#   m1= b.min()
#   m2 = b.max()
#   return a*(m2-m1) + m1

# def mean_squared_error(y_predicted,y_actual):
#   return ((y_predicted-y_actual)**2).sum()/(len(y_predicted))

# print('Following are the commands you may enter :')
# while(True):
#   print("0. If you want to terminate")
#   print("1. If you want to know the actual stock price")
#   print("2. If you want to know a range of stock price")
#   input_from_user=int(input("Enter the command : "))
#   if(input_from_user==0):
#     break
#   elif(input_from_user==1):
#     company_name = input('Enter company name : ')
#     with open('gru_overall','rb') as f:
#       mo = pickle.load(f)
#     for layer in mo.layers:
#       layer.trainable = False
#     ticker_symbol = company_name.upper()+".NS"
#     days_back = 15
#     interval='15m'
#     end_date = datetime.datetime.now().strftime('%Y-%m-%d')
#     start_date = (datetime.datetime.now() - datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
#     company_data=yf.download(ticker_symbol, start=start_date, end=end_date,interval=interval)['Close']
#     df=scaler.fit_transform(np.array(company_data).reshape(-1,1))
#     new_data=pd.DataFrame()
#     df=np.array(df)
#     l = []
#     for i in range(df.shape[0]):
#       l.append(df[i][0])
#     new_data['Close']=l
#     new_data=pd.DataFrame(new_data,columns=["Close"])
#     def create_dataset(X, y, time_steps=1):
#       Xs, ys = [], []
#       for i in range(len(X) - time_steps):
#           Xs.append(X.iloc[i:(i + time_steps)].values)
#           ys.append(y.iloc[i + time_steps])
#       return np.array(Xs), np.array(ys)
#     X_test,y_test = create_dataset(new_data[['Close']], new_data[['Close']],60)
#     mo.fit(X_test, y_test,epochs=10, batch_size=8)
#     hh = (mo.predict(X_test))
#     pred=inverse(hh,company_data)
#     p=pred.flatten()
#     y_predicted=np.array(p)
#     comp_data=list(company_data)
#     y_actual=np.array(comp_data[60:])
#     print()
#     print()
#     print(f'Mean Squared Error for {company_name} is {mean_squared_error(y_predicted,y_actual)}')
#     print()
#     print()
#     new_x_test=np.array(new_data[len(company_data) - 60:]).reshape(1,60,1)
#     pred=mo.predict(new_x_test)
#     next_predicted=inverse(pred,company_data)[0][0]
#     print()
#     print()
#     print("Next day's prediction: ",next_predicted)
#     print()
#     print()

#   elif(input_from_user==2):
#     company_name = input('Enter company name : ')
#     predictions=[]
#     for i in range(5):
#       with open('gru_overall','rb') as f:
#         mo = pickle.load(f)
#       for layer in mo.layers:
#         layer.trainable = False
#       ticker_symbol = company_name.upper()+".NS"
#       days_back = 15
#       interval='15m'
#       end_date = datetime.datetime.now().strftime('%Y-%m-%d')
#       start_date = (datetime.datetime.now() - datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
#       company_data=yf.download(ticker_symbol, start=start_date, end=end_date,interval=interval)['Close']
#       df=scaler.fit_transform(np.array(company_data).reshape(-1,1))
#       new_data=pd.DataFrame()
#       df=np.array(df)
#       l = []
#       for i in range(df.shape[0]):
#         l.append(df[i][0])
#       new_data['Close']=l
#       new_data=pd.DataFrame(new_data,columns=["Close"])

#       def create_dataset(X, y, time_steps=1):
#         Xs, ys = [], []
#         for i in range(len(X) - time_steps):
#             Xs.append(X.iloc[i:(i + time_steps)].values)
#             ys.append(y.iloc[i + time_steps])
#         return np.array(Xs), np.array(ys)
#       X_test,y_test = create_dataset(new_data[['Close']], new_data[['Close']],60)
#       mo.fit(X_test, y_test,epochs=10,batch_size=8,verbose=True)
#       hh = (mo.predict(X_test))
#       pred=inverse(hh,company_data)
#       p=pred.flatten()
#       y_predicted=np.array(p)
#       comp_data=list(company_data)
#       y_actual=np.array(comp_data[60:])
#       print()
#       print()
#       print(f'Mean Squared Error for {company_name} is {mean_squared_error(y_predicted,y_actual)}')
#       print()
#       print()
#       new_x_test=np.array(new_data[len(company_data) - 60:]).reshape(1,60,1)
#       pred=mo.predict(new_x_test)
#       next_predicted=inverse(pred,company_data)[0][0]
#       predictions.append(next_predicted)
#     predictions=np.array(predictions)
#     mean=predictions.mean()
#     standard_deviation=predictions.std()
#     print(f'Stock Price is supposed to be in range : [ {mean-standard_deviation} , {mean+standard_deviation} ]')

