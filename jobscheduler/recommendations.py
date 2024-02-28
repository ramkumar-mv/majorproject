import numpy as np
import pickle
from datetime import datetime, timedelta, date
from firebase_admin import auth
from firebase.firebase import (
    getNToday,
    getPToday,
    getKToday,
    getTempToday,
    getHumToday,
    getpHToday,
    getRainToday,
    getArea,
    getRegion,
    getCrop,
    getCropConfirm,
    insertRecommendation,
    insertPrediction,
)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
from firebase_admin import firestore

def executeRecommendations():
    # executing empty sample job
    for user in auth.list_users().iterate_all():
        print(user.uid)
        thresholdValue(user.uid)
        thresholdRes(user.uid)
        thresholdPred(user.uid)
        thresholdNPK(user.uid)
        #thresholdHum(user.uid)

def thresholdValue(userId):
    db = firestore.client()
    
    # Define the user ID
    user_id = "3FoNl6M7Yycgx4LUGqt33tVb6Vf2"
    
    # Define the paths to store the data
    paths = {
        "nitrogen": f"/userInfo/{user_id}/nitrogenTotals",
        "phosp": f"/userInfo/{user_id}/phosTotals",
        "pottasium": f"/userInfo/{user_id}/potassiumTotals",
        "ph": f"/userInfo/{user_id}/pHTotals",
        "rainfall": f"/userInfo/{user_id}/rainTotals"
    }
    
        # Function to update Firestore
    def update_firestore(event):
        data = event.data
        for key, value in data.items():
            doc_ref = db.document(paths[key])
            print("reference",doc_ref)
            doc_ref.set({"value": value})
        print("Data updated in Firestore.")
    
    # Reference to the Realtime Database
    ref = firebase_db.reference("/test")
    
    # Listen for changes in the Realtime Database
    ref.listen(update_firestore)


def thresholdRes(userId):
    report = ""
    area = getArea(userId)
    reg = area['total']
    
    region = getRegion(userId)
    reg1 = region['value']

    crop = getCrop(userId)
    reg2 = crop['value']

    data = getNToday(userId)
    nitrogen_value = data['Nitrogen']
    
    data1 = getPToday(userId)
    phos_value = data1['Phosphorous']

    data2 = getKToday(userId)
    pot_value = data2['Potassium']

    data3 = getTempToday(userId)
    temp_value = data3['Temperature']

    data4 = getHumToday(userId)
    hum_value = data4['Humidity']

    data5 = getpHToday(userId)
    pvalue = data5['pH']

    data6 = getRainToday(userId)
    rain = data6['Rain']

    data7 = getCropConfirm(userId)
    cropConfirm = data7['value']
    

    if reg1 == "North":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])
    
        with open('capstoneApi/RandomForest_North.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('north',prediction)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)
        else:
            report += f"We have predicted {prediction} for your land. "

    elif reg1 == "South":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])
    
        with open('capstoneApi/RandomForest_South.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('south',prediction)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)
        else:
            report += f"We have predicted {prediction} for your land. "

    elif reg1 == "West":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_West.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('west',prediction)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)
        else:
            report += f"We have predicted {prediction} for your land. "

    elif reg1 == "East":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_East.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('east',prediction)
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)
        else:
            report += f"We have predicted {prediction} for your land. "

    return insertPrediction(userId, report)

def thresholdPred(userId):
    report = ""
    area = getArea(userId)
    reg = area['total']
    print(reg)
    
    region = getRegion(userId)
    reg1 = region['value']
    print(reg1)

    crop = getCrop(userId)
    reg2 = crop['value']
    print(reg2)

    data = getNToday(userId)
    nitrogen_value = data['Nitrogen']
    
    data1 = getPToday(userId)
    phos_value = data1['Phosphorous']

    data2 = getKToday(userId)
    pot_value = data2['Potassium']

    data3 = getTempToday(userId)
    temp_value = data3['Temperature']

    data4 = getHumToday(userId)
    hum_value = data4['Humidity']

    data5 = getpHToday(userId)
    pvalue = data5['pH']

    data6 = getRainToday(userId)
    rain = data6['Rain']

    data7 = getCropConfirm(userId)
    cropConfirm = data7['value']
    

    if reg1 == "North":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])
    
        with open('capstoneApi/RandomForest_North.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('north',prediction)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)

        if cropConfirm not in ['Wheat', 'Maize']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field(North)"
            final = None
        elif cropConfirm == 'wheat' and prediction == 'wheat':
            report += "We have also predicited Wheat, Let's go on to the next step"
            final = 'Wheat'
        elif prediction == 'maize' and cropConfirm == 'maize':
            report += "We have also predicited Maize, Let's go on to the next step"
            final = 'Maize'
        else:
            pass
            
    elif reg1 == "South":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_South.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('south',prediction)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)

        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_South.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        
        if cropConfirm not in ['Rice', 'Maize', 'Cotton']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field(South)"
            final = None
        elif prediction == 'rice' and cropConfirm == 'Rice':
            report += "We have also predicited Rice, Let's go on to the next step"
            final = 'Rice'
        elif prediction == 'maize' and cropConfirm == 'Maize':
            report += "We have also predicited Maize, Let's go on to the next step"
            final = 'Maize'
        elif prediction == 'cotton' and cropConfirm == 'Cotton':
            report += "We have also predicited Cotton, Let's go on to the next step"
            final = 'Cotton'
        else:
            pass

    elif reg1 == "West":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_West.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('west',prediction)
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)
        
        if cropConfirm not in ['Rice', 'Wheat']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field(West)"
            final = None
        elif prediction == 'rice' and cropConfirm == 'Rice':
            report += "We have also predicited Rice, Let's go on to the next step"
            final = 'Rice'
        elif cropConfirm == 'Wheat' and prediction == 'wheat':
            report += "We have also predicited Wheat, Let's go on to the next step"
            final = 'Wheat'
        else:
            pass

    elif reg1 == "East":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_East.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        print('east',prediction)
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)
        
        if cropConfirm not in ['Rice', 'Wheat', 'Cotton']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field(East)"
            final = None
        elif prediction == 'rice' and cropConfirm == 'Rice':
            report += "We have also predicited Rice, Let's go on to the next step"
            final = 'Rice'
        elif cropConfirm == 'wheat' and prediction == 'Wheat':
            report += "We have also predicited Wheat, Let's go on to the next step"
            final = 'Wheat'
        elif prediction == 'cotton' and cropConfirm == 'Cotton':
            report += "We have also predicited Cotton, Let's go on to the next step"
            final = 'Cotton'
        else:
            pass
    else:
        pass

    return final, insertPrediction(userId, report)

def thresholdNPK(userId):
    report = ""
    
    data = getNToday(userId)
    nitrogen_value = data['Nitrogen']
    date_value = data['date']
    
    data1 = getPToday(userId)
    phos_value = data1['Phosphorous']

    data2 = getKToday(userId)
    pot_value = data2['Potassium']

    data3 = getTempToday(userId)
    temp_value = data3['Temperature']

    data4 = getHumToday(userId)
    hum_value = data4['Humidity']

    data5 = getpHToday(userId)
    pvalue = data5['pH']

    data6 = getRainToday(userId)
    rain = data6['Rain']

    final, _ = thresholdPred(userId)
    
    if final == 'Rice':
        a = nitrogen_value - 120
        b = phos_value - 30
        c = pot_value - 30
        
        report += f"{date_value} : "
        report += f"Your Nitrogen value is {nitrogen_value}, the difference between the ideal Nitrogen value is {a:.2f}. \n"
        report += f"Your Phosphorous value is {phos_value}, the difference between the ideal Phosphorous value is {b:.2f}. \n"
        report += f"Your Potassium value is {pot_value}, the difference between the ideal Potassium value is {c:.2f}. \n"
        report += f"The Temperature today is {temp_value} and the humidity today is {hum_value}. \n"
        report += f"The pH value is {pvalue}. \n"
        report += "You have to use DAP for this amount and MOP for this amount. \n"
        
        if pvalue < 7:
            report += f"The soil is acidic. \n"
        elif pvalue > 7:
            report += f"The soil is Alkaline. \n"
        else:
            report += f"The soil is neutral. \n"
            
        if rain < 300:
            report += "Heavy rain warning. \n"
        elif rain <500:
            report += "Moderate Rain. \n"
        else:
            report += "No rain. \n"
    
        return insertRecommendation(userId, report)

    elif final == 'Wheat':
        a = nitrogen_value - 80
        b = phos_value - 40
        c = pot_value - 40
        
        report += f"{date_value} : \n"
        report += f"Your Nitrogen value is {nitrogen_value}, the difference between the ideal Nitrogen value is {a:.2f}. \n"
        report += f"Your Phosphorous value is {phos_value}, the difference between the ideal Phosphorous value is {b:.2f}. \n"
        report += f"Your Potassium value is {pot_value}, the difference between the ideal Potassium value is {c:.2f}. \n"
        report += f"The Temperature today is {temp_value} and the humidity today is {hum_value}. \n"
        report += f"The pH value is {pvalue}. \n"
        report += "You have to use DAP for this amount and MOP for this amount. \n"
        
        if pvalue < 7:
            report += f"The soil is acidic. \n"
        elif pvalue > 7:
            report += f"The soil is Alkaline. \n"
        else:
            report += f"The soil is neutral. \n"
            
        if rain < 300:
            report += "Heavy rain warning. \n"
        elif rain <500:
            report += "Moderate Rain. \n"
        else:
            report += "No rain. \n"
    
        return insertRecommendation(userId, report)

    elif final == 'Maize':
        a = nitrogen_value - 120
        b = phos_value - 60
        c = pot_value - 40
        
        report += f"{date_value} : \n"
        report += f"Your Nitrogen value is {nitrogen_value}, the difference between the ideal Nitrogen value is {a:.2f}. \n"
        report += f"Your Phosphorous value is {phos_value}, the difference between the ideal Phosphorous value is {b:.2f}. \n"
        report += f"Your Potassium value is {pot_value}, the difference between the ideal Potassium value is {c:.2f}. \n"
        report += f"The Temperature today is {temp_value} and the humidity today is {hum_value}. \n"
        report += f"The pH value is {pvalue}. \n"
        report += "You have to use DAP for this amount and MOP for this amount. \n"
        
        if pvalue < 7:
            report += f"The soil is acidic. \n"
        elif pvalue > 7:
            report += f"The soil is Alkaline. \n"
        else:
            report += f"The soil is neutral. \n"
            
        if rain < 300:
            report += "Heavy rain warning. \n"
        elif rain <500:
            report += "Moderate Rain. \n"
        else:
            report += "No rain. \n"
    
        return insertRecommendation(userId, report)

    elif final == 'Cotton':
        a = nitrogen_value - 50
        b = phos_value - 30
        c = pot_value - 35
        
        report += f"{date_value} : \n"
        report += f"Your Nitrogen value is {nitrogen_value}, the difference between the ideal Nitrogen value is {a:.2f}. \n"
        report += f"Your Phosphorous value is {phos_value}, the difference between the ideal Phosphorous value is {b:.2f}. \n"
        report += f"Your Potassium value is {pot_value}, the difference between the ideal Potassium value is {c:.2f}. \n"
        report += f"The Temperature today is {temp_value} and the humidity today is {hum_value}. \n"
        report += f"The pH value is {pvalue}. \n"
        report += "You have to use DAP for this amount and MOP for this amount. \n"
        
        if pvalue < 7:
            report += f"The soil is acidic. \n"
        elif pvalue > 7:
            report += f"The soil is Alkaline. \n"
        else:
            report += f"The soil is neutral. \n"
            
        if rain < 300:
            report += "Heavy rain warning. \n"
        elif rain <500:
            report += "Moderate Rain. \n"
        else:
            report += "No rain \n"

    elif final == None:
        report += "Prediction Loading..."

    return insertRecommendation(userId, report)
