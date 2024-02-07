import numpy as np
import pickle
from datetime import datetime, timedelta, date
from firebase_admin import auth
from firebase.firebase import (
    getN,
    getP,
    getK,
    getTempN,
    getHumN,
    getpH,
    getRain,
    getNToday,
    getPPrevDay,
    getKPrevDay,
    getTempNPrevDay,
    getHumNPrevDay,
    getpHPrevDay,
    getRainPrevDay,
    insertRecommendation,
)

def executeRecommendations():
    # executing empty sample job
    for user in auth.list_users().iterate_all():
        print(user.uid)
        thresholdNPK(user.uid)
        #thresholdHum(user.uid)


def thresholdNPK(userId):
    report = ""
    #userId = "xR4Afu2Av5NS5HsA8R880zYfJgk1"
    #previous_day_nitrogen = getNPrevDay(userId)
    #report += f"Previous day's Nitrogen: {previous_day_nitrogen}"

    #t = date.today().strftime("%Y-%m-%d")
    N = getNToday(userId)
    '''P = getP(userId, t)
    K = getK(userId, t)
    temp = getTempN(userId, t)
    hum = getHumN(userId, t)
    pH = getpH(userId, t)
    rain = getRain(userId, t)'''

    report += f"Your Nitrogen value is {N}"
    '''report += f"Your Phosphorous value is {P}"
    report += f"Your Potassium value is {K}"
    report += f"The Temperature today is {temp} and the humidity today is {hum}"
    #report += f"Predicted crop: {prediction}'''
    '''
    # Check for NaN or None values in the data
    if any(v is None or np.isnan(v) for v in [N, P, K, temp, hum, pH, rain]):
        report += "Some input values are missing or NaN. Unable to make prediction."
        return insertRecommendation(userId, report)

    data = np.array([[N, P, K, temp, hum, pH, rain]])

    with open('capstoneApi/RandomForest.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    
    prediction = loaded_model.predict(data)  # Pass the 2D array as input
    if prediction != 'rice':
        a = N - 79.89
        b = P - 47.58
        c = K - 39.87
        report += f"Your Nitrogen value is {N}, the difference between the ideal Nitrogen value for paddy is {a:.2f} "
        report += f"Your Phosphorous value is {P}, the difference between the ideal Phosphorous value for paddy is {b:.2f}"
        report += f"Your Potassium value is {K}, the difference between the ideal Potassium value for paddy is {c:.2f}"
        report += f"The Temperature today is {temp} and the humidity today is {hum}"
        report += f"We recommend {prediction}"
    else:
        report += f"Your Nitrogen value is {N}"
        report += f"Your Phosphorous value is {P}"
        report += f"Your Potassium value is {K}"
        report += f"The Temperature today is {temp} and the humidity today is {hum}"
        report += f"Predicted crop: {prediction}"'''

    return insertRecommendation(userId, report)

    
    '''
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
        )'''

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
