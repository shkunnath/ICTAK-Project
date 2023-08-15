import numpy as np
import pandas as pd
from flask import Flask, request, render_template, session
import pickle

X = ['NumberOfDeviceRegistered', 'NumberOfAddress', 'CashbackAmount',
       'Tenure', 'WarehouseToHome', 'DaySinceLastOrder',
       'PreferredLoginDevice_Computer', 'PreferredLoginDevice_Mobile Phone',
       'CityTier_1', 'CityTier_2', 'CityTier_3', 'PreferredPaymentMode_Cash on Delivery',
       'PreferredPaymentMode_Credit Card', 'PreferredPaymentMode_Debit Card',
       'PreferredPaymentMode_E wallet', 'PreferredPaymentMode_UPI',
       'Gender_Female', 'Gender_Male',
       'PreferedOrderCat_Fashion', 'PreferedOrderCat_Grocery',
       'PreferedOrderCat_Laptop & Accessory', 'PreferedOrderCat_Mobile Phone', 'PreferedOrderCat_Others',
       'SatisfactionScore_1', 'SatisfactionScore_2', 'SatisfactionScore_3',
       'SatisfactionScore_4', 'SatisfactionScore_5',
       'MaritalStatus_Divorced', 'MaritalStatus_Married', 'MaritalStatus_Single', 'Complain_0',
       'Complain_1']
len(X)

def predict_price(tenure, warehouse, numdevice, numaddress, lastorder, cashback, logindevice, citytier, paymentmode, ordercat, score, maritalstatus, gender, complain):    
    logindevice_index = X.index('PreferredLoginDevice_' + logindevice)
    citytier_index = X.index('CityTier_' + citytier)
    paymentmode_index = X.index('PreferredPaymentMode_' + paymentmode)
    gender_index = X.index('Gender_' + gender)
    ordercat_index = X.index('PreferedOrderCat_' + ordercat)
    score_index = X.index('SatisfactionScore_' + score)
    maritalstatus_index = X.index('MaritalStatus_' + maritalstatus)
    complain_index = X.index('Complain_' + complain)

    index_list = [logindevice_index, citytier_index, paymentmode_index, gender_index, ordercat_index, score_index, maritalstatus_index, complain_index]

    x = np.zeros(len(X))
    x[0] = numdevice
    x[1] = numaddress
    x[2] = cashback
    x[3] = tenure
    x[4] = warehouse
    x[5] = lastorder

    for ind in index_list:
      if ind >= 0:
          x[ind] = 1

    data = scaler.transform(x.reshape(1,-1))
    return model.predict(data)[0]


app = Flask(__name__)
app.secret_key = '2chai4vada6samosa'

model = pickle.load(open('adaboost_best_raw.pkl', 'rb'))
scaler = pickle.load(open('scaler_raw.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        tenure = float(request.form['tenure'])
        warehouse = float(request.form['warehousetohome'])
        numdevice = float(request.form['numdevices'])
        numaddress = float(request.form['numaddress'])
        lastorder = float(request.form['lastorder'])
        cashback = float(request.form['cashbackamount'])
        logindevice = request.form['logindevice']
        citytier = request.form['citytier']
        paymentmode = request.form['paymentmode']
        ordercat = request.form['ordercat']
        score = request.form['satisfactionscore']
        maritalstatus =request.form['maritalstatus']
        gender = request.form['gender']
        complain = request.form['complain']
        show_table = True
  
    prediction = predict_price(tenure, warehouse, numdevice, numaddress, lastorder, cashback, logindevice, citytier, paymentmode, ordercat, score, maritalstatus, gender, complain)    
  
    return render_template('index.html', prediction=prediction, tenure=tenure, warehouse=warehouse,numdevice=numdevice,numaddress=numaddress,lastorder=lastorder,cashback=cashback,
                           logindevice=logindevice,citytier=citytier,paymentmode=paymentmode,ordercat=ordercat,score=score,maritalstatus=maritalstatus,gender=gender,complain=complain,show_table=show_table)

@app.route('/fill_form_from_excel', methods=['GET'])
def fill_form_from_excel():
    df = pd.read_excel('data.xlsx')
    if 'current_row' not in session:
        session['current_row'] = 0
    
    current_row = session['current_row']
    row = df.iloc[current_row]

    session['current_row'] += 1

    tenure = row['Tenure']
    warehouse = row['WarehouseToHome']
    numdevice = row['NumberOfDeviceRegistered']
    numaddress = row['NumberOfAddress']
    lastorder = row['DaySinceLastOrder']
    cashback = row['CashbackAmount']
    logindevice = row['PreferredLoginDevice']
    citytier = row['CityTier']
    paymentmode = row['PreferredPaymentMode']
    ordercat = row['PreferedOrderCat']
    score = row['SatisfactionScore']
    maritalstatus = row['MaritalStatus']
    gender = row['Gender']
    complain = row['Complain']

    return render_template('filled_form.html', tenure=tenure, warehouse=warehouse,numdevice=numdevice,numaddress=numaddress,lastorder=lastorder,cashback=cashback,
                           logindevice=logindevice,citytier=citytier,paymentmode=paymentmode,ordercat=ordercat,score=score,maritalstatus=maritalstatus,gender=gender,complain=complain)

if __name__ == "__main__":
    app.run(debug=True)