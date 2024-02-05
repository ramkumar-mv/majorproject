from firebase_admin import auth
from firebase.firebase import (
    getDietPrevWeek,
    getWaterPrevWeek,
    getOilPrevWeek,
    getHousehold,
    getTempPrevWeek,
    insertRecommendation,
)
from jobscheduler.constants import diet, badDiet, meat, veggie


def executeRecommendations():
    # executing empty sample job
    for user in auth.list_users().iterate_all():
        print(user.uid)
        #thresholdDiet(user.uid)
        #thresholdWater(user.uid)
        #thresholdOil(user.uid)
        #thresholdHousehold(user.uid)
        thresholdTemp(user.uid)
        thresholdHum(user.uid)
        


'''def thresholdDiet(userId):
    report = ""
    # get week of data
    data = getDietPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d["total"] for d in data])

    # check if greater than weekly avg canadian
    if weeklyTotal > 43534:
        report += (
            "DIET: Your weekly total is "
            + str(weeklyTotal / 1000)
            + "kg, which is above what the avg Canadian is supposed to produce. You can refer to our suggestions for further tips!.\n"
        )
    else:
        report = (
            "DIET: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 43.53kg a week and you produced "
            + str(weeklyTotal / 1000)
            + "kg."
        )
    with open('carbon_weight_prediction_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Calculate the predicted value for tomorrow
    input_data = [[weeklyTotal]]
    total_oil_consumption = sum(day.get("total", 0) for day in data)
    prediction = loaded_model.predict(input_data)
    positive_prediction = [abs(value) for value in prediction]
    report += f"The predicted value for tomorrow is {positive_prediction[0]:.2f} kg."

    # Give them suggestions
    report += "We recommend to follow a diet."

    return insertRecommendation(userId, report)

    # check worst and best categories
    meat_carbon, veggie_carbon, bad_carbon = 0, 0, 0
    for d in data:
        for m in meat:
            if m in d:
                meat_carbon += d[m] * diet[m]
        for v in veggie:
            if v in d:
                veggie_carbon += d[v] * diet[v]
        for b in badDiet:
            if b in d:
                bad_carbon += d[b] * diet[b]

    # check if meat is above recommended portion
    if (meat_carbon / weeklyTotal) * 100 > 25:
        report += (
            "Canada's Food Guide recommends that 25\% of your plate consist of meat. \nWe noticed that over 25\% of your diet consist of meat: "
            + str(int((meat_carbon / weeklyTotal) * 100))
            + "\%. If you care to reduce your carbon emissions, we highly consider reducing how much meat you consume.\n"
        )
    # check if veggie is below recommended portion
    if (veggie_carbon / weeklyTotal) * 100 < 50:
        report += (
            "Canada's Food Guide recommends that 50\% of your plate consist of fruits, veggies, and legumes.\nWe noticed that your veggie intake is les than 50\%: "
            + str(int((veggie_carbon / weeklyTotal) * 100))
            + "\%. If you care to reduce your carbon emissions, we highly consider increasing how much fruits and veggies you consume. You can also sub out meat protein for plant protein.\n"
        )

    # check how much of their meals comes from high producing sources
    report += (
        "Finally, "
        + str(int((bad_carbon / weeklyTotal) * 100))
        + '\% of what you ate this week came from our "top 7 worst foods for the environment" list: Beef, Lamb, Shellfish, Chocolate, Dairy, Fish.\n'
    )

    return insertRecommendation(userId, report)


def thresholdHousehold(userId):
    report = ""
    # get data
    data = getHousehold()
    # get total carbon
    dailyTotalCarbon = sum([d["carbon"] for d in data])
    # get time on per each room
    dailyDurationRoom1 = sum(
        [d["duration"] if d["room"] == "room1" else 0 for d in data]
    )
    dailyDurationRoom2 = sum(
        [d["duration"] if d["room"] == "room2" else 0 for d in data]
    )
    dailyDurationRoom3 = sum(
        [d["duration"] if d["room"] == "room3" else 0 for d in data]
    )
    dailyDurationRoom4 = sum(
        [d["duration"] if d["room"] == "room4" else 0 for d in data]
    )
    # get total time on in the day
    dailyDuration = sum([d["duration"] for d in data])

    # check if it's greater than the avg canadian
    if dailyTotalCarbon > 8493.15:
        report += (
            "HOUSEHOLD: Your daily total is "
            + str(int(dailyTotalCarbon / 1000))
            + "kg which is above what the avg Canadian is supposed to produce. here are our suggestions for further tips!.\n"
        )
    else:
        report = (
            "HOUSEHOLD: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 8.49kg a week and you produced "
            + str(round(dailyTotalCarbon / 1000, 1))
            + "kg."
        )
    with open('elec_weight_dataset.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Calculate the predicted value for tomorrow
    input_data = [[dailyTotalCarbon]]
    total_oil_consumption = sum(day.get("total", 0) for day in data)
    prediction = loaded_model.predict(input_data)
    positive_prediction = [abs(value) for value in prediction]
    report += f"The predicted value for tomorrow is {positive_prediction[0]:.2f} kg."

    # Give them suggestions
    report += "We recommend using household appliances a little less."

    return insertRecommendation(userId, report)
    # find which light is used the least and most
    if dailyDuration / 60 > 5:
        report += (
            "We noticed you have your lights running for "
            + str(round(dailyDuration / 3600, 1))
            + "h today. Let's see if there is a light you can turn off!\n"
        )

        lights = [
            (dailyDurationRoom1 / dailyDuration, "room1"),
            (dailyDurationRoom2 / dailyDuration, "room2"),
            (dailyDurationRoom3 / dailyDuration, "room3"),
            (dailyDurationRoom4 / dailyDuration, "room4"),
        ]

        lights.sort(key=lambda x: x[0])
        report += (
            "We noticed you use"
            + lights[0][1]
            + " the least, is there anyway to minimize this more? We also noticed you use "
            + lights[-1][1]
            + " the most. Could this be cut down or put on to our scheduler to ensure it gets used only when needed.\n\n"
        )
        report += "Other recommendations we have are to switch to LEDs if you already have not.\nUse energy efficient appliances. \nTurn off lights that are not used or automate them."

    return insertRecommendation(userId, report)


def thresholdWater(userId):
    report = ""

    # Make an API request to get the prediction and water consumption data
    response = wresult(request=None, user_id=userId)

    if response.status_code == 200:
        result_data = response.data

        # Retrieve the prediction and water consumption data from the response
        prediction = result_data.get('prediction', [])
        water_data_prev_week = result_data.get('water_data_prev_week', [])
        weeklyTotal = sum([d["total"] for d in water_data_prev_week])

        # Calculate the threshold limit (e.g., 80% of the weekly limit)
        threshold_limit = 0.8 * 637000  # 80% of the average Canadian's usage

        # Add the predicted value to the report message
        report += (
            f"WATER CONSUMPTION: You have crossed {int((weeklyTotal / 637000) * 100)}% of the weekly water consumption limit. Your weekly total is "
            + str(int(weeklyTotal / 1000))
            + "kg, which is close to the average Canadian's usage."
            + f" The predicted value for tomorrow is {prediction[0]:.2f} kg. Here are some recommendations for reducing your water consumption.\n"
        )
    report += "We recommend to use water appliances a little less."

    return insertRecommendation(userId, report)
import pickle
def thresholdWater(userId):
    report = ""
    # get week of data
    data = getWaterPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d["total"] for d in data])

    # check if more than avg canadian
    if weeklyTotal > 637000:
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
        )
    # give them suggestions
    with open('water_pred_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Calculate the predicted value for tomorrow
    input_data = [[weeklyTotal]]  # Wrap weeklyTotal in a list to create a 2D array
    total_water_consumption = sum(day.get("total", 0) for day in data)
    prediction = loaded_model.predict(input_data)  # Pass the 2D array as input
    positive_prediction = [abs(value) for value in prediction]
    report += f"The predicted value for tomorrow is {positive_prediction[0]:.2f} kg."

    # Give them suggestions
    report += "We recommend using water appliances a little less."

    return insertRecommendation(userId, report)'''
import pickle
def thresholdHum(userId):
    report = ""
    # get week of data
    data = getOilPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d["total"] for d in data])

    # check if more than avg canadian
    '''if weeklyTotal > 840000:
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
        )'''
    # give them suggestions
    with open('capstoneApi/model_hum.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Calculate the predicted value for tomorrow
    input_data = [80]
    total_oil_consumption = sum(day.get("total", 0) for day in data)
    prediction = loaded_model.predict(input_data)
    positive_prediction = [abs(value) for value in prediction]
    report += f"Today your humidity is {input_data} The predicted value for tomorrow is {positive_prediction[0]:.2f}."

    # Give them suggestions
    #report += "We recommend using gas appliances a little less."

    return insertRecommendation(userId, report)

def thresholdTemp(userId):
    report = ""
    # get week of data
    data = getTempPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d["total"] for d in data])

    # check if more than avg canadian
    '''if data > 637000:
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
    report += f"Today your temperature is {22} The predicted temperature for tomorrow is {positive_prediction[0]:.2f} and
                Today your humidity is {73} The predicted humidity for tomorrow is {positive_prediction1[0]:.2f} ."

    # Give them suggestions
    #report += "We recommend using water appliances a little less."

    return insertRecommendation(userId, report)
