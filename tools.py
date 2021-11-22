# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 17:30:09 2021

@author: 82104
"""
import numpy as np
import pandas as pd

def BOP(data): 
    BOP_data = (data['close'] - data['open'])/(data['high']-data['low'])
    return BOP_data


def MFI(data,period=14):
    typical_price = (data['close']+data['high']+data['low'])/3
    money_flow = typical_price*data['volume']
    positive_flow = []
    negative_flow = []
    for i in range(1,len(typical_price)):
        if typical_price[i] > typical_price[i-1]:
            positive_flow.append(money_flow[i])#참고한 링크에서는 여기가 money_flow[i-1]인데 money_flow[i]가 맞겠지? 업비트랑 비슷하게 할려면 money_flow[i]로 하는게 맞음
            negative_flow.append(0)
        elif typical_price[i] < typical_price[i-1]:
            negative_flow.append(money_flow[i])#money_flow[i-1]?
            positive_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(0)
    positive_mf = []
    negative_mf = []
    for i in range(period-1,len(positive_flow)):
        positive_mf.append(sum(positive_flow[i+1-period : i+1]))
    for i in range(period-1,len(negative_flow)):
        negative_mf.append(sum(negative_flow[i+1-period : i+1]))
    #mfi = 100 * np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf))
    mfi = 100 - 100 / (1 +  (np.array(positive_mf)/np.array(negative_mf)))
    return [float('Nan')]*period+list(mfi)


def Stochastic_Fast_K(data,n=14):
    fast_k = ((data['close'] - data['low'].rolling(n).min()) / (data['high'].rolling(n).max() - data['low'].rolling(n).min()))*100
    #slow_k = fast_k.rolling(n).mean() #뭘 의미하는지 모르겠음
    #slow_d = slow_k.rolling(n).mean() #뭘 의미하는지 모르겠음
    return fast_k

def RSI(data,period= 14):
    delta = data['close'].diff()
    ups,downs = delta.copy(), delta.copy()
    ups[ups<0] = 0
    downs[downs>0] = 0
    AU = ups.ewm(com = period-1,min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD    
    return pd.Series(100-(100/(1+RS)),name = 'RSI')