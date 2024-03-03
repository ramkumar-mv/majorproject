from firebase_admin import initialize_app, credentials, firestore, db
from datetime import datetime, timedelta, date
import random

# Use a service account
cred = credentials.Certificate(
    "majorproject-60694-firebase-adminsdk-ntugr-075c8c8205.json"
)
initialize_app(
    cred, {"databaseURL": "https://majorproject-60694-default-rtdb.firebaseio.com",
          "projectId": "majorproject-60694"}
)

##### Region #######

def getRegion(userId: str):
    database = firestore.client()
    doc_ref = (
        database.collection('details')
        .document(userId)
        .collection('Totals')
        .document('regionTotals')
    )
    doc = doc_ref.get()

    region = {}
    if doc.exists:
        region = doc.to_dict()

    if 'total' not in region:
        region['total'] = 0
    
    print('Region',region)
    return region

##### Area #######

def getArea(userId: str):
    database = firestore.client()
    doc_ref = (
        database.collection('details')
        .document(userId)
        .collection('Totals')
        .document('areaTotals')
    )
    doc = doc_ref.get()

    area = {}
    if doc.exists:
        area = doc.to_dict()

    if 'total' not in area:
        area['total'] = 0
    print('Area',area)
    return area

##### Crop #######

def getCrop(userId: str):
    database = firestore.client()
    doc_ref = (
        database.collection('details')
        .document(userId)
        .collection('Totals')
        .document('cropTotals')
    )
    doc = doc_ref.get()

    crop = {}
    if doc.exists:
        crop = doc.to_dict()

    if 'total' not in crop:
        crop['total'] = 0
    print('crop',crop)
    return crop

##### ConfirmCrop #######

def getCropConfirm(userId: str):
    database = firestore.client()
    doc_ref = (
        database.collection('details')
        .document(userId)
        .collection('Totals')
        .document('cropConfirm')
    )
    doc = doc_ref.get()

    cropConfirm = {}
    if doc.exists:
        cropConfirm = doc.to_dict()

    if 'total' not in cropConfirm:
        cropConfirm['total'] = 0
        
    print('Confirmed Crop',cropConfirm)
    return cropConfirm


##### Nitrogen #######

def getN(userId: str, datestamp: str):
    database = firestore.client()
    a = date.today().strftime("%Y-%m-%d")
    doc_ref = (
        database.collection('userInfo')
        .document(userId)
        .collection('nitrogenTotals')
        .document(datestamp)
    )
    doc = doc_ref.get()
    print("doc1:",doc)

    nitrogen = {}
    if doc.exists:
        nitrogen = doc.to_dict()
        nitrogen['date'] = datestamp

    if 'total' not in nitrogen:
        nitrogen['total'] = 0
    print('Nitrogen', nitrogen)
    return nitrogen


def getNToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getN(userId, formatted_date)
    else:
        return getN(userId, date.today().strftime("%Y-%m-%d"))


def getNPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getN(userId, yesterday.strftime("%Y-%m-%d"))


def getNPrevWeek(userId: str):
    nitrogen = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        nitrogen.append(getN(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    nitrogen.append(getN(userId, date.today().strftime("%Y-%m-%d")))

    return nitrogen


def getNPrevMonth(userId: str):
    nitrogen = []

    # get previous 6 days
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        nitrogen.append(getN(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    nitrogen.append(getN(userId, date.today().strftime("%Y-%m-%d")))

    return nitrogen

####### phosphorus #######
def getP (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection('userInfo')
        .document(userId)
        .collection('phosTotals')
        .document(datestamp)
    )
    doc = doc_ref.get()

    phos = {}
    if doc.exists:
        phos = doc.to_dict()
        phos['date'] = datestamp

    if 'total' not in phos:
        phos['total'] = 0

    print("Phos",phos)

    return phos
    
def getPToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getP(userId, formatted_date)
    else:
        return getP(userId, date.today().strftime("%Y-%m-%d"))
    
def getPPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)
    return getP (userId, yesterday.strftime("%Y-%m-%d"))
    
def getPPrevWeek(userId: str):
    phos = []
    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        phos.append(getP(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    phos.append(getP(userId, date.today().strftime("%Y-%m-%d")))
    return phos

def getPPrevMonth(userId: str):
    phos = []
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        phos.append(getP(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    phos.append(getP(userId, date.today().strftime("%Y-%m-%d")))
    return phos

####### Potassium #######
def getK (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection('userInfo')
        .document(userId)
        .collection('potassiumTotals')
        .document(datestamp)
    )
    doc = doc_ref.get()
    potas = {}
    if doc.exists:
        potas = doc.to_dict()
        potas['date'] = datestamp

    if 'total' not in potas:
        potas['total'] = 0

    print("Pot", potas)
    return potas

def getKToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getK(userId, formatted_date)
    else:
        return getK(userId, date.today().strftime("%Y-%m-%d"))
    
def getKPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)
    return getK (userId, yesterday.strftime("%Y-%m-%d"))

def getKPrevWeek(userId: str):
    potas = []
    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        potas.append(getP(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    potas.append(getP(userId, date.today().strftime("%Y-%m-%d")))
    return potas

def getKPrevMonth(userId: str):
    potas = []
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        potas.append(getP(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    potas.append(getP(userId, date.today().strftime("%Y-%m-%d")))
    return potas

####### temperature #######
def getTemp(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection('userInfo')
        .document(userId)
        .collection('temperatureTotals')
        .document(datestamp)
    )
    doc = doc_ref.get()
    temp = {}
    if doc.exists:
        temp = doc.to_dict()
        temp['date'] = datestamp

    if "total" not in temp:
        temp['total'] = 0

    print("Temp",temp)

    return temp

def getTempToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getTemp(userId, formatted_date)
    else:
        return getTemp(userId, date.today().strftime("%Y-%m-%d"))


def getTempPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getTemp(userId, yesterday.strftime("%Y-%m-%d"))

def getTempPrevWeek(userId: str):
    temp = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        temp.append(getTemp(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    temp.append(getTemp(userId, date.today().strftime("%Y-%m-%d")))

    return temp

def getTempPrevMonth(userId: str):
    temp = []
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        temp.append(getTemp(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    temp.append(getTemp(userId, date.today().strftime("%Y-%m-%d")))
    return temp

####### Humidity #######
def getHum(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("humidityTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()

    hum = {}
    if doc.exists:
        hum = doc.to_dict()
        hum["date"] = datestamp

    if "total" not in hum:
        hum["total"] = 0

    return hum

def getHumToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getHum(userId, formatted_date)
    else:
        return getHum(userId, date.today().strftime("%Y-%m-%d"))

def getHumPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getHum(userId, yesterday.strftime("%Y-%m-%d"))

def getHumPrevWeek(userId: str):
    hum = []
    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        hum.append(getHum(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    hum.append(getHum(userId, date.today().strftime("%Y-%m-%d")))
    return hum

def getHumPrevMonth(userId: str):
    hum = []
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        hum.append(getHum(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    hum.append(getHum(userId, date.today().strftime("%Y-%m-%d")))
    return hum

####### pH #######
def getpH(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("pHTotals")
        .document(datestamp)
    )
    doc = doc_ref.get()
    pH = {}
    if doc.exists:
        pH = doc.to_dict()
        pH["date"] = datestamp

    if "total" not in pH:
        pH["total"] = 0

    return pH

def getpHToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getpH(userId, formatted_date)
    else:
        return getpH(userId, date.today().strftime("%Y-%m-%d"))

def getpHPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getpH(userId, yesterday.strftime("%Y-%m-%d"))

def getpHPrevWeek(userId: str):
    pH = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        pH.append(getpH(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    pH.append(getpH(userId, date.today().strftime("%Y-%m-%d")))
    return pH


def getpHPrevMonth(userId: str):
    pH = []
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        pH.append(getpH(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    pH.append(getpH(userId, date.today().strftime("%Y-%m-%d")))
    return pH

####### rainfall #######
def getRain (userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = (
        database.collection("userInfo")
        .document(userId)
        .collection("rainTotals")
        .document(datestamp)
    )

    doc = doc_ref.get()

    rain = {}
    if doc.exists:
        rain = doc.to_dict()
        rain["date"] = datestamp

    if "total" not in rain:
        rain["total"] = 0

    return rain

def getRainToday(userId: str):
    current_date = datetime.now()
    # Check if the day is between 1 and 9
    if current_date.day < 10:
        # Use padding for the day
        formatted_date = current_date.strftime("%Y-%m-%-d")
        return getRain(userId, formatted_date)
    else:
        return getRain(userId, date.today().strftime("%Y-%m-%d"))
        
def getRainPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getRain(userId, yesterday.strftime("%Y-%m-%d"))

def getRainPrevWeek(userId: str):
    rain = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        rain.append(getRain(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    rain.append(getRain(userId, date.today().strftime("%Y-%m-%d")))

    return rain


def getRainPrevMonth(userId: str):
    rain = []
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        rain.append(getRain(userId, day.strftime("%Y-%m-%d")))
    # get todays date
    rain.append(getRain(userId, date.today().strftime("%Y-%m-%d")))
    return rain

###### Transportation #######


def getTransportation(userId: str, datestamp: str):
    database = firestore.client()
    doc_ref = database.collection(u'userInfo').document(
        userId).collection(u'transportTotals').document(datestamp)
    doc = doc_ref.get()

    transportation = {}
    if doc.exists:
        transportation = doc.to_dict()
        transportation['date'] = datestamp

    if 'total' not in transportation:
        transportation['total'] = 0

    return transportation


def getTransportationPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getTransportation(userId, yesterday.strftime("%Y-%m-%d"))


def getTransportationPrevWeek(userId: str):
    transportation = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        transportation.append(getTransportation(
            userId, day.strftime("%Y-%m-%d")))

    # get todays date
    transportation.append(getTransportation(
        userId, date.today().strftime("%Y-%m-%d")))

    return transportation


def getTransportationPrevMonth(userId: str):
    transportation = []

    # get previous 6 days
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        transportation.append(getTransportation(
            userId, day.strftime("%Y-%m-%d")))

    # get todays date
    transportation.append(getTransportation(
        userId, date.today().strftime("%Y-%m-%d")))

    return transportation



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

####### RECOMMENDATION #######

def insertPrediction(userId: str, data):
    database = firestore.client()
    doc_ref = database.collection("predictions").document(userId)

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
