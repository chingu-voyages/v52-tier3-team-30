import datetime

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="v52-tier3-team-30")

DOC_NAME = '2024'

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
    })

    print('Resident created')



