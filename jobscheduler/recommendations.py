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

def executeRecommendations():
    # executing empty sample job
    for user in auth.list_users().iterate_all():
        print(user.uid)
        thresholdNPK(user.uid)
        thresholdPred(user.uid)
        #thresholdHum(user.uid)

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
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)

        if cropConfirm not in ['wheat', 'maize']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field"
        elif cropConfirm == 'wheat' and prediction == 'wheat':
            report += "We have also predicited Wheat, Let's go on to the next step"
            final = 'wheat'
        elif prediction == 'maize' and cropConfirm == 'maize':
            report += "We have also predicited Maize, Let's go on to the next step"
            final = 'maize'
        else:
            pass
            
    elif reg1 == "South":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_South.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)

        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_South.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        
        if cropConfirm not in ['rice', 'maize', 'cotton']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field"
        elif prediction == 'rice' and cropConfirm == 'rice':
            report += "We have also predicited Rice, Let's go on to the next step"
            final = 'rice'
        elif prediction == 'maize' and cropConfirm == 'maize':
            report += "We have also predicited Maize, Let's go on to the next step"
            final = 'maize'
        elif prediction == 'cotton' and cropConfirm == 'cotton':
            report += "We have also predicited Cotton, Let's go on to the next step"
            final = 'cotton'
        else:
            pass

    elif reg1 == "West":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_West.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)

        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_West.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        
        if cropConfirm not in ['rice', 'wheat']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field"
        elif prediction == 'rice' and cropConfirm == 'rice':
            report += "We have also predicited Rice, Let's go on to the next step"
            final = 'rice'
        elif cropConfirm == 'wheat' and prediction == 'wheat':
            report += "We have also predicited Wheat, Let's go on to the next step"
            final = 'wheat'
        else:
            pass

    elif reg1 == "East":
        data = np.array([[nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]])

        with open('capstoneApi/RandomForest_East.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        prediction = loaded_model.predict(data)
        
        if any(v is None or np.isnan(v) for v in [nitrogen_value,phos_value,pot_value, temp_value, hum_value, pvalue, rain]):
            report += "Some input values are missing or NaN. Unable to make prediction."
            return insertPrediction(userId, report)

        
        if cropConfirm not in ['rice', 'wheat', 'cotton']:
            report += "With these NPK and weather conditions you can't grow the desired crop in this field"
        elif prediction == 'rice' and cropConfirm == 'rice':
            report += "We have also predicited Rice, Let's go on to the next step"
            final = 'rice'
        elif cropConfirm == 'wheat' and prediction == 'wheat':
            report += "We have also predicited Wheat, Let's go on to the next step"
            final = 'wheat'
        elif prediction == 'cotton' and cropConfirm == 'cotton':
            report += "We have also predicited Cotton, Let's go on to the next step"
            final = 'cotton'
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

    elif final == 'wheat':
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

    elif final == 'maize':
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

    elif final == 'cotton':
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
            report += "No rain. \n"
    
        return insertRecommendation(userId, report)

'''import pickle
def thresholdHum(userId):
    report = ""
    # get week of data
    data = getOilPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d["total"] for d in data])

    # check if more than avg canadian
    if weeklyTotal > 840000:
        report += (
            "OIL CONSUMPTION: Your weekly total is "
            + str(int(weeklyTotal / 1000))
            + "kg which is above what the avg Canadian is supposed to produce. here are our suggestions for further tips!.\n"
        )
    elif 672000 < weeklyTotal < 840000:
        report += (
            "OIL CONSUMPTION: You have crossed 80% of the weekly oil consumption limit. Your weekly total is "
            + str(int(weeklyTotal / 1000))
            + "kg, which is close to the average Canadian's usage. Here are some recommendations for reducing your oil consumption.\n"
        )
    else:
        report = (
            "OIL CONSUMPTION: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 840.00kg a week and you produced "
            + str(round(weeklyTotal / 1000, 1))
            + "kg."
        )
    # give them suggestions
    with open('capstoneApi/model_hum.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Calculate the predicted value for tomorrow
    input_data = [80]
    total_oil_consumption = sum(day.get("total", 0) for day in data)
    prediction = loaded_model.predict(input_data)
    positive_prediction = [abs(value) for value in prediction]
    report += f"Today your humidity is {input_data} The predicted value for tomorrow is {positive_prediction[0]:.2f}."

    return insertRecommendation(userId, report)'''

'''def thresholdTemp(userId):
    report = ""
    # get week of data
    data = getTempPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d["total"] for d in data])

    # check if more than avg canadian
    if data > 637000:
        report += (
            f"WATER CONSUMPTION: You have crossed {int((weeklyTotal / 637000) * 100)}% of the weekly water consumption limit. Your weekly total is "
            + str(int(weeklyTotal / 1000))
            + "kg, which is close to the average Canadian's usage."
        )
    elif 509600 < weeklyTotal < 637000:
        report += (
            f"WATER CONSUMPTION: You have crossed {int((weeklyTotal / 637000) * 100)}% of the weekly water consumption limit. Your weekly total is "
            + str(int(weeklyTotal / 1000))
            + "kg, which is close to the average Canadian's usage."
        )
    else:
        report += (
            f"WATER CONSUMPTION: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 637.00kg a week and you produced "
            + str(round(weeklyTotal / 1000, 1))
            + "kg, which is very good."
        )'
    # give them suggestions
    with open('capstoneApi/model_temp.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Calculate the predicted value for tomorrow
    input_data = [[22]]  # Wrap weeklyTotal in a list to create a 2D array
    input_data1 = [[73]]
    total_temp_consumption = sum(day.get("total", 0) for day in data)
    prediction = loaded_model.predict(input_data)  # Pass the 2D array as input
    positive_prediction = [abs(value) for value in prediction]

    prediction1 = loaded_model.predict(input_data1)  # Pass the 2D array as input
    positive_prediction1 = [abs(value) for value in prediction1]
    report += f"Today your temperature is {22} The predicted temperature for tomorrow is {positive_prediction[0]:.2f} and Today your humidity is {73} The predicted humidity for tomorrow is {prediction1[0]:.2f} ."

    # Give them suggestions
    #report += "We recommend using water appliances a little less."

    return insertRecommendation(userId, report)'''
