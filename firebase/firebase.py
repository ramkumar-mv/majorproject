from firebase_admin import initialize_app, credentials, firestore, db
from datetime import datetime, timedelta, date
import random

# Use a service account
cred = credentials.Certificate(
    "test-40a5d-firebase-adminsdk-c7pf4-b2c2f06868.json"
)
initialize_app(
    cred, {"databaseURL": "https://test-40a5d-default-rtdb.firebaseio.com"}
)

####### Nitrogen #######
def getN (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    nitro = {}
    if doc.exists:
        nitro_data = doc.to_dict()
        nitro = nitro_data.get("Nitrogen")
    return nitro

def getNPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getN (userId, yesterday.strftime("%Y-%m-%d"))

####### phosphorus #######
def getP (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    phos = {}
    if doc.exists:
        phos_data = doc.to_dict()
        phos = phos_data.get("Phosphorus")
    return phos

def getPPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getP (userId, yesterday.strftime("%Y-%m-%d"))

####### Potassium #######
def getK (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    pot = {}
    if doc.exists:
        pot_data = doc.to_dict()
        pot = pot_data.get("Phosphorus")
    return pot

def getKPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getK (userId, yesterday.strftime("%Y-%m-%d"))

####### temperature #######
def getTempN(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    temp1 = {}
    if doc.exists:
        temp_data1 = doc.to_dict()
        temp1 = temp_data1.get("Temperature")

    return temp1


def getTempNPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getTempN(userId, yesterday.strftime("%Y-%m-%d"))

####### Humidity #######
def getHumN(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    hum1 = {}
    if doc.exists:
        hum_data1 = doc.to_dict()
        hum1 = hum_data1.get("Humidity")

    return hum1

def getHumNPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getHumN(userId, yesterday.strftime("%Y-%m-%d"))

####### pH #######
def getpH(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    pH = {}
    if doc.exists:
        pH_data = doc.to_dict()
        pH = pH_data.get("pH")

    return pH

def getpHPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getpH(userId, yesterday.strftime("%Y-%m-%d"))

####### rainfall #######
def getRain (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("nutrientsTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    rain = {}
    if doc.exists:
        rain_data = doc.to_dict()
        rain = rain_data.get("pH")

    return rain

def getRainPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getpH(userId, yesterday.strftime("%Y-%m-%d"))

####### temperature #######
def getTemp(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("TempValues")
        .document(datestamp)
    )
    doc = doc_ref.get()

    temp = {}
    if doc.exists:
        temp_data = doc.to_dict()
        temp = temp_data.get("Temperature")

    return temp


def getTempPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getTemp(userId, yesterday.strftime("%Y-%m-%d"))
 


####### RECOMMENDATION #######

def insertRecommendation(userId: str, data):
    database = firestore.client()
    doc_ref = database.collection("recommendations").document(userId)

    doc = doc_ref.get()

    if doc.exists:
        doc_data = doc.to_dict()
        if doc_data is not None and "counter" in doc_data:
            counter = doc_data["counter"]
        else:
            counter = 0
        doc_ref.update({str(counter): data, "counter": firestore.Increment(1)})
    else:
        doc_ref.set(
            {
                "0": data,
                "counter": 1,
            }
        )

    doc = doc_ref.get()

    return doc.to_dict()



"""def insertRecommendation(userId: str, data):
    database = firestore.client()
    doc_ref = database.collection("recommendations").document(userId)

    doc = doc_ref.get()

    if doc.to_dict() == {}:
        doc_ref.set(
            {
                "0": data,
                "counter": 1,
            }
        )
    else:
        d = doc.to_dict()
        doc_ref.update({str(d["counter"]): data, "counter": firestore.Increment(1)})

    doc = doc_ref.get()

    return doc.to_dict()"""


def getSuggestion(category: str):  # get suggestion for provided data
    if category == "" or category is None:
        return ""

    database = firestore.client()

    suggestions = {}
    recommendation = ""

    doc_ref = database.collection("suggestions").document(category)
    doc = doc_ref.get()

    suggestions = doc.to_dict()
    recommendation = random.choice(suggestions["suggestions"])

    return recommendation
