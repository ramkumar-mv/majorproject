from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import sys

from jobscheduler.lights import (
    pauseLight,
    resumeLight,
    setWeekdayLightOn,
    setWeekdayLightOff,
    setWeekendLightOn,
    setWeekendLightOff,
)
from jobscheduler.thermostat import (
    pauseThermostat,
    resumeThermostat,
    setWeekdayThermostatOn,
    setWeekdayThermostatOff,
    setWeekendThermostatOn,
    setWeekendThermostatOff,
)
from firebase.firebase import (
    getLights,
    getLight,
    insertLight,
    getTemps,
    insertTemp,
    insertLightDuration,
    setLight,
    setTemp,
    getTemp,
)

@api_view(["GET"])
def api_overview(request):
    data = {
        "all_entries": "getLights/",
        "single_entry": "getLight/<str:pk>/",
        "create_entry": "insertLight/",
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_lights(request, room):
    try:
        entries = getLights(room)
        return Response(data=entries, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_light(request, room):
    try:
        entry = getLight(room)
        return Response(data=entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def set_light(request, room, cmd):
    try:
        lastOn = getLight(room)
        res = setLight(room, cmd)

        entry = insertLight(res)

        if cmd == "off":
            entry = insertLightDuration(room, lastOn)

        return Response(data=entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def insert_light(request):
    try:
        print(request.data)
        entry = insertLight(request.data)
        return Response(data=entry, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekday_schedule_light_on(request, room, time):
    try:
        print(room, time)
        res = setWeekdayLightOn(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekend_schedule_light_on(request, room, time):
    try:
        print(room, time)
        res = setWeekendLightOn(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekday_schedule_light_off(request, room, time):
    try:
        print(room, time)
        res = setWeekdayLightOff(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekend_schedule_light_off(request, room, time):
    try:
        print(room, time)
        res = setWeekendLightOff(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def pause_schedule_light(request, room):
    try:
        print(room)
        res = pauseLight(room)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def resume_schedule_light(request, room):
    try:
        print(room)
        res = resumeLight(room)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###### THERMOSTAT ######


@api_view(["GET"])
def get_temps(request):
    try:
        entries = getTemps()
        return Response(data=entries, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_temp(request):
    try:
        lastest_entry = getTemp()
        return Response(data=lastest_entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def set_temp(request, temp):
    try:
        res = setTemp(temp)
        print(res)
        entry = insertTemp(res)
        return Response(data=entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def insert_temp(request):
    try:
        data = {
            "temp": request.data["temp"],
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        entry = insertTemp(data)

        return Response(data=entry, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekday_schedule_thermostat_on(request, temp, time):
    try:
        print(temp, time)
        res = setWeekdayThermostatOn(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekend_schedule_thermostat_on(request, temp, time):
    try:
        print(temp, time)
        res = setWeekendThermostatOn(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekday_schedule_thermostat_off(request, temp, time):
    try:
        print(temp, time)
        res = setWeekdayThermostatOff(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def set_weekend_schedule_thermostat_off(request, temp, time):
    try:
        print(temp, time)
        res = setWeekendThermostatOff(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def pause_schedule_thermostat(request):
    try:
        res = pauseThermostat()
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def resume_schedule_thermostat(request):
    try:
        res = resumeThermostat()
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from django.http import JsonResponse 
import pickle
from firebase.firebase import getWaterPrevWeek,getOilPrevWeek

@api_view(["GET"])
def hresult(request):
    user_id = 'AW1SqKbAdnPwZfgbTiAULxunIro1'
    water_prev_week_data = getWaterPrevWeek(user_id)
    total_water_consumption = sum(day.get("total", 0) for day in water_prev_week_data)
    with open('model_hum.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
        
    input_data = [[total_water_consumption]]
    prediction = loaded_model.predict(input_data)
    response_data = {'prediction': prediction.tolist()}
    return JsonResponse(response_data)

@api_view(["GET"])
def tresult(request):
    user_id = 'AW1SqKbAdnPwZfgbTiAULxunIro1'
    oil_prev_week_data = getOilPrevWeek(user_id)
    total_oil_consumption = sum(day.get("total", 0) for day in oil_prev_week_data)
    
    with open('model_temp.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    input_data = [[total_oil_consumption]]
    prediction = loaded_model.predict(input_data)
    positive_prediction = [abs(value) for value in prediction]
    
    response_data = {'prediction': positive_prediction}
    return JsonResponse(response_data)

"""@api_view(["GET"])
def gresult(request):
        with open('linear_regression_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        input_data = [[3.11]]
        prediction = loaded_model.predict(input_data)

        response_data = {'prediction': prediction.tolist()}
        return JsonResponse(response_data)"""
    

"""@api_view(["GET"])
def wresult(request):
        with open('water_pred_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
            
        input_data = [[1000]]

        prediction = loaded_model.predict(input_data)

        response_data = {'prediction': prediction.tolist()}
        return JsonResponse(response_data)"""

