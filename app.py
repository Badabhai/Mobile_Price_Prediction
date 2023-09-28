import streamlit as st
import pickle
import numpy as np
import pandas as pd

pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("Mobile Price Detector")

model = st.selectbox("Mobile Brand",df['model'].unique())
Ram = st.selectbox("Ram(In GB)",[6,2,3,4,8,12,16,18])
Rom = st.selectbox("Internal Memory(In GB)",[128,4,8,16,32,64,256,512,1024])
Network = st.selectbox("Network",["5G","4G","3G"])
Processor = st.selectbox("Processor Brand",["Snapdragon","Dimensity","Helio","Bionic","Exynos","Others"])
Camera = st.selectbox("Camera",["Triple","Quad","Dual","Mono"])
Primary = st.number_input("Primary Camera Pixel(upto 200)",value=64)
Front = st.selectbox("Front Camera",["Yes","No"])
Fast_Charging = st.selectbox("Fast Charging",["Yes","No"])
Refresh_rate = st.selectbox("Refresh Rate",["120 Hz","90 Hz","60 Hz","144 Hz"])
Fold = st.selectbox("Foldable Display",["No","Yes"])
mAh = st.number_input("Battery Capacity(In mAh)",value=5000)
Inch = st.number_input("Screen Size(in Inches)",value=6.59)
resolution = st.selectbox("Screen Resolution",['1080x1920','1080x2400','480x800', '640x1136', '720x1280','720x1600', '750x1334','1440x2560'])


if st.button("Predict Price"):
    # Getting Network selected
    if Network == "5G" :
        five_G,four_G,three_G = 1,1,1
    elif Network == "4G" :
        five_G,four_G,three_G = 0,1,1
    else:
        five_G,four_G,three_G = 0,0,1

    # Getting Processor Selected
    if Processor == "Snapdragon":
        Snapdragon,Dimensity,Helio,Exynos,Bionic = 1,0,0,0,0
    elif Processor == "Dimensity":
        Snapdragon,Dimensity,Helio,Exynos,Bionic = 0,1,0,0,0
    elif Processor == "Helio":
        Snapdragon,Dimensity,Helio,Exynos,Bionic = 0,0,1,0,0
    elif Processor == "Exynos":
        Snapdragon,Dimensity,Helio,Exynos,Bionic = 0,0,0,1,0
    elif Processor == "Bionic":
        Snapdragon,Dimensity,Helio,Exynos,Bionic = 0,0,0,0,1
    elif Processor == "Others":
        Snapdragon,Dimensity,Helio,Exynos,Bionic = 0,0,0,0,0

    # Getting Camera Type
    if Camera == "Quad":
        Quad,Triple,Dual = 1,0,0
    elif Camera == "Triple":
        Quad,Triple,Dual = 0,1,0
    elif Camera == "Dual":
        Quad,Triple,Dual = 0,0,1
    elif Camera == "Mono":
        Quad,Triple,Dual = 0,0,0

    # Front Camera 
    if Front == "Yes":
        Front = 1
    else:
        Front= 0
    
    # Refresh Rate of Screen
    if Refresh_rate == "144 Hz":
        One44=1
        One20=0
        Ninety=0
    elif Refresh_rate == "120 Hz":
        One44=0
        One20=1
        Ninety=0
    elif Refresh_rate == "90 Hz":
        One44=0
        One20=0
        Ninety=1
    else:
        One44=0
        One20=0
        Ninety=0

    # Foldable Screen 
    if Fold == "Yes":
        Fold = 1
    else:
        Fold = 0

    # Fast Charging 
    if Fast_Charging == "Yes":
        Fast_Charing = 1
    else:
        Fast_Charing = 0

    #Screen Resolution
    x_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[1])

    #  Making an array of details
    query = np.array([model,Ram,five_G,four_G,three_G,Snapdragon,Dimensity,Helio,Exynos,Bionic,Rom,Fast_Charing,str(mAh),Quad,Triple,Dual,Front,str(Primary),One44,One20,Ninety,Fold,Inch,y_res,x_res])
    query= query.reshape(1,25)
    df1 = pd.DataFrame(query,columns =['model','ram','5G','4G','3G','Snapdragon','Dimensity','Helio','Exynos','Bionic','Rom','Fast_Charing','mAh','Quad','Triple','Dual','FC','PC','144Hz','120Hz','90Hz','Fold','inch','y_res','x_res'])
    df1['ram'] = df1["ram"].astype('float64')
    df1['Rom'] = df1["Rom"].astype('float64')
    df1['inch'] = df1["inch"].astype('float64')
    df1['5G'] = df1['5G'].astype('int64')
    df1['4G'] = df1['4G'].astype('int64')
    df1['3G'] = df1['3G'].astype('int64')
    df1['Snapdragon'] = df1['Snapdragon'].astype('int64')
    df1['Dimensity'] = df1['Dimensity'].astype('int64')
    df1['Helio'] = df1['Helio'].astype('int64')
    df1['Exynos'] = df1['Exynos'].astype('int64')
    df1['Bionic'] = df1['Bionic'].astype('int64')
    df1['Fast_Charing'] = df1['Fast_Charing'].astype('int64')
    df1['Quad'] = df1['Quad'].astype('int64')
    df1['Triple'] = df1['Triple'].astype('int64')
    df1['Dual'] = df1['Dual'].astype('int64')
    df1['FC'] = df1['FC'].astype('int64')
    df1['144Hz'] = df1['144Hz'].astype('int64')
    df1['120Hz'] = df1['120Hz'].astype('int64')
    df1['90Hz'] = df1['90Hz'].astype('int64')
    df1['Fold'] = df1['Fold'].astype('int64')
    df1['y_res'] = df1['y_res'].astype('int64')
    df1['x_res'] = df1['x_res'].astype('int64')

    # Predicting the Price using ML
    Price = pipe.predict(df1)
    st.write("The Predicted Price is :  ₹" + str(int(Price)))