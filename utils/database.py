import datetime
import json
import requests

from geopy.geocoders import Nominatim

import os


ROUTEXL_USERNAME = os.getenv("ROUTEXL_USERNAME")
ROUTEXL_PASSWORD = os.getenv("ROUTEXL_PASSWORD")
ROUTEXL_URL = 'https://api.routexl.com/tour/'


geolocator = Nominatim(user_agent="v52-tier3-team-30")

DOC_NAME = '2024'

def get_dict(docs):
    output = {}
    for doc in docs:
        d = doc.to_dict()
        points = d['address']
        d['id'] = doc.id
        location = geolocator.reverse(f"{points[0]}, {points[1]}")
        output[location.address] = d

    return output


def get_coords(data):
    coords = []
    print(data)
    for d in data:
        points = get_geopoint(d)
        temp = {"address": f"{d}", "lat": f"{points[0]}", "lng": f"{points[1]}"}
        coords.append(temp)

    return json.dumps(coords)


def get_optimised_route(data):
    coords = get_coords(data)

    input_data = f"locations={coords}"

    session = requests.Session()
    session.auth = (ROUTEXL_USERNAME, ROUTEXL_PASSWORD)
    #auth = session.post('https://' + 'api.routexl.com/tour/')
    response = session.post(ROUTEXL_URL, data=input_data)

    res_json = json.loads(response.content)

    return res_json['route']


def get_geopoint(address):
    location = geolocator.geocode(address)
    return [location.latitude, location.longitude]


def convert_timestamp(timeslot, preferred_date):
    datetime_str = preferred_date + ' ' + timeslot
    datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

    return datetime_obj


def get_status(db, requestId):
    doc_ref = db.collection("residents").document(requestId)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()

    return None


def update_request(db, requestId, position, status, timestamp):
    update_queue(db, requestId, position)
    update_status(db, requestId, status)
    update_timestamp(db, requestId, timestamp)


def update_timestamp(db, requestId, timestamp):
    doc_ref = db.collection("residents").document(requestId)
    doc_ref.update({"timeslot": timestamp})


def update_queue(db, requestId, position):
    doc_ref = db.collection("residents").document(requestId)
    doc_ref.update({"queue": position})


def update_status(db, requestId, status):
    doc_ref = db.collection("residents").document(requestId)
    doc_ref.update({"status": status})


def get_all_requests(db):
    docs = db.collection("residents").stream()
    return docs


def calculate_time(today, duration):
    return today + datetime.timedelta(minutes=duration)


def get_order(route, data, db):
    output = []

    sgtTimeDelta = datetime.timedelta(hours=8)
    sgtTZObject = datetime.timezone(sgtTimeDelta, name="SGT")
    today_date = datetime.date.today()
    today = datetime.datetime(today_date.year, today_date.month, today_date.day, hour=8, minute=0, second=0, microsecond=0, tzinfo=sgtTZObject)
    t1 = today.astimezone(datetime.timezone(sgtTimeDelta))
    arrival = 0
    for key, obj in route.items():
        t1 = calculate_time(t1, obj['arrival'] - arrival)
        arrival = obj['arrival']
        curr = data[obj['name']]
        resident_id = curr['id']
        update_request(db, resident_id, key, "Scheduled", t1)


def create_today_listings(db):
    today_date = datetime.date.today()
    today = datetime.datetime(today_date.year, today_date.month, today_date.day)
    query = db.collection("residents").where("timeslot", ">=", today).where("timeslot", "<", today + datetime.timedelta(days=1))
    if query:
        print('here')
        docs = (query.stream())
        data = get_dict(docs)
        route = get_optimised_route(data)
        print(route)
        get_order(route, data, db)


def get_output(docs):
    output = {}
    for doc in docs:
        d = doc.to_dict()
        output[doc.id] = d

    return output


def get_today_listings(db):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    doc_ref = db.collection("appointments").document(today)
    doc = doc_ref.get()
    if not doc.exists:
        doc_ref.set({"isCreated": False}, merge=True)

    d = doc.to_dict()
    if not d['isCreated']:
        create_today_listings(db)
        doc_ref.set({"isCreated": True}, merge=True)

    today_date = datetime.date.today()
    today_obj = datetime.datetime(today_date.year, today_date.month, today_date.day)
    query = db.collection("residents").where("timeslot", ">=", today_obj).where("timeslot", "<", today_obj + datetime.timedelta(days=1))
    docs = (query.stream())
    return get_output(docs)


def create_resident(db, name, email, phone, address, timeslot, preferred_date):

    timestamp = convert_timestamp(timeslot, preferred_date)
    geopoint = get_geopoint(address)

    doc_ref = db.collection('residents')
    update_time, resident_ref = doc_ref.add({
        'name': name,
        'email': email,
        'phone': phone,
        'address': geopoint,
        'timeslot': timestamp,
        'status': 'Submitted',
        'queue': 0
    })

    return resident_ref.id




