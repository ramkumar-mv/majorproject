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
    user_id = userId

    current_date = datetime.now()
    if current_date.day < 10:
        formatted_date = current_date.strftime("%Y-%m-%-d")
    else:
        formatted_date =  date.today().strftime("%Y-%m-%d")
    
    # Define the paths to store the data
    paths = {
        "nitrogen": f"userInfo/{user_id}/nitrogenTotals/{formatted_date}",
        "phosp": f"userInfo/{user_id}/phosTotals/{formatted_date}",
        "pottasium": f"userInfo/{user_id}/potassiumTotals/{formatted_date}",
        "ph": f"userInfo/{user_id}/pHTotals/{formatted_date}",
        "rainfall": f"userInfo/{user_id}/rainTotals/{formatted_date}"
    }
    
    # Function to update Firestore
    def update_firestore(event):
        data = event.data
        for key, value in data.items():
            # Construct full path with collection ID and document ID
            collection, document = paths[key].split('/', 1)
            doc_ref = db.collection(collection).document(document)
            print("reference", doc_ref)
            doc_ref.set({"total": value})
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
    nitrogen_value = data['total']
    
    data1 = getPToday(userId)
    phos_value = data1['total']

    data2 = getKToday(userId)
    pot_value = data2['total']

    data3 = getTempToday(userId)
    temp_value = data3['total']

    data4 = getHumToday(userId)
    hum_value = data4['total']

    data5 = getpHToday(userId)
    pvalue = data5['total']

    data6 = getRainToday(userId)
    rain = data6['total']
    

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
    nitrogen_value = data['total']
    
    data1 = getPToday(userId)
    phos_value = data1['total']

    data2 = getKToday(userId)
    pot_value = data2['total']

    data3 = getTempToday(userId)
    temp_value = data3['total']

    data4 = getHumToday(userId)
    hum_value = data4['total']

    data5 = getpHToday(userId)
    pvalue = data5['total']

    data6 = getRainToday(userId)
    rain = data6['total']

    data7 = getCropConfirm(userId)
    cropConfirm = data7['value']

    final = None  # Default value for final

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
        report += f"Invalid region: {reg1}. Unable to make a prediction."

    print('final at pred: ',final)

    return final, insertPrediction(userId, report)

def thresholdNPK(userId):
    report = ""
    
    data = getNToday(userId)
    nitrogen_value = data['total']
    
    data1 = getPToday(userId)
    phos_value = data1['total']

    data2 = getKToday(userId)
    pot_value = data2['total']

    data3 = getTempToday(userId)
    temp_value = data3['total']

    data4 = getHumToday(userId)
    hum_value = data4['total']

    data5 = getpHToday(userId)
    pvalue = data5['total']

    data6 = getRainToday(userId)
    rain = data6['total']

    data7 = getArea(userId)
    area = data7['total']
    print(area)

    current_date = datetime.now()
    if current_date.day < 10:
        date_value = current_date.strftime("%Y-%m-%-d")
    else:
        date_value =  date.today().strftime("%Y-%m-%d")
    

    final, _ = thresholdPred(userId)
    print('final at report: ',final)
    
    if final == 'Rice':
        a = nitrogen_value - 120
        b = phos_value - 30
        c = pot_value - 30
        d = (b*100)/46
        e = a - d 
        f = (c*100)/60
        g = (e*100)/46
        
        report += f"{date_value} : "
        report += f"Your Nitrogen value is {nitrogen_value} kg/ha, the difference between the ideal Nitrogen value is {a:.2f} kg/ha. \n"
        report += f"Your Phosphorous value is {phos_value} kg/ha, the difference between the ideal Phosphorous value is {b:.2f} kg/ha. \n"
        report += f"Your Potassium value is {pot_value} kg/ha, the difference between the ideal Potassium value is {c:.2f} kg/ha. \n"
        report += f"The Temperature today is {temp_value} C and the humidity today is {hum_value} %. \n"
        report += f"The pH value is {pvalue}. \n"
        if g >= 0 and d >= 0 and f >= 0:
            report += f"You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif g < 0 and d >= 0 and f >= 0:
            report += f" Urea is excess already ,You have to use DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif d < 0 and g >= 0 and f >= 0:
            report += f"DAP is excess already ,You have to use Urea for {g:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif f < 0 and g >= 0 and d >= 0:
            report += f"MOP is excess already ,You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha \n"
        
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
        d = (b*100)/46
        e = a - d 
        f = (c*100)/60
        g = (e*100)/46
        
        report += f"{date_value} : \n"
        report += f"Your Nitrogen value is {nitrogen_value} kg/ha, the difference between the ideal Nitrogen value is {a:.2f} kg/ha. \n"
        report += f"Your Phosphorous value is {phos_value} kg/ha, the difference between the ideal Phosphorous value is {b:.2f} kg/ha. \n"
        report += f"Your Potassium value is {pot_value} kg/ha, the difference between the ideal Potassium value is {c:.2f} kg/ha. \n"
        report += f"The Temperature today is {temp_value} C and the humidity today is {hum_value} %. \n"
        report += f"The pH value is {pvalue}. \n"
        if g >= 0 and d >= 0 and f >= 0:
            report += f"You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif g < 0 and d >= 0 and f >= 0:
            report += f" Urea is excess already ,You have to use DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif d < 0 and g >= 0 and f >= 0:
            report += f"DAP is excess already ,You have to use Urea for {g:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif f < 0 and g >= 0 and d >= 0:
            report += f"MOP is excess already ,You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha \n"
                
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
        d = (b*100)/46
        e = a - d 
        f = (c*100)/60
        g = (e*100)/46
        
        report += f"{date_value} : \n"
        report += f"Your Nitrogen value is {nitrogen_value} kg/ha, the difference between the ideal Nitrogen value is {a:.2f} kg/ha. \n"
        report += f"Your Phosphorous value is {phos_value} kg/ha, the difference between the ideal Phosphorous value is {b:.2f} kg/ha. \n"
        report += f"Your Potassium value is {pot_value} kg/ha, the difference between the ideal Potassium value is {c:.2f} kg/ha. \n"
        report += f"The Temperature today is {temp_value} C and the humidity today is {hum_value} %. \n"
        report += f"The pH value is {pvalue}. \n"
        if g >= 0 and d >= 0 and f >= 0:
            report += f"You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif g < 0 and d >= 0 and f >= 0:
            report += f" Urea is excess already ,You have to use DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif d < 0 and g >= 0 and f >= 0:
            report += f"DAP is excess already ,You have to use Urea for {g:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif f < 0 and g >= 0 and d >= 0:
            report += f"MOP is excess already ,You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha \n"
        
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
        d = (b*100)/46
        e = a - d 
        f = (c*100)/60
        g = (e*100)/46
        
        report += f"{date_value} : \n"
        report += f"Your Nitrogen value is {nitrogen_value} kg/ha, the difference between the ideal Nitrogen value is {a:.2f} kg/ha. \n"
        report += f"Your Phosphorous value is {phos_value} kg/ha, the difference between the ideal Phosphorous value is {b:.2f} kg/ha. \n"
        report += f"Your Potassium value is {pot_value} kg/ha, the difference between the ideal Potassium value is {c:.2f} kg/ha. \n"
        report += f"The Temperature today is {temp_value} C and the humidity today is {hum_value} %. \n"
        report += f"The pH value is {pvalue}. \n"
        if g >= 0 and d >= 0 and f >= 0:
            report += f"You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif g < 0 and d >= 0 and f >= 0:
            report += f" Urea is excess already ,You have to use DAP for {d:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif d < 0 and g >= 0 and f >= 0:
            report += f"DAP is excess already ,You have to use Urea for {g:.2f} kg/ha and MOP for {f:.2f} kg/ha \n"
        elif f < 0 and g >= 0 and d >= 0:
            report += f"MOP is excess already ,You have to use Urea for {g:.2f} kg/ha and DAP for {d:.2f} kg/ha \n"
        
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
