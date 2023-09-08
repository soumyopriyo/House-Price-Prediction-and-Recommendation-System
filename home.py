import pickle
import json
import numpy as np
from os import path

location = None
city= None
model = None


def load_saved_attributes():

    global city_values
    global location_values
    global model

    with open("columns.json", "r") as f:
        resp = json.load(f)
        location_values = resp["Location"]
        city_values = resp["City"]
        

    model = pickle.load(open("model.pkl", "rb"))

def get_location_names():
    #if location_values == None:
    #  load_saved_attributes()
    return location_values

def get_city_values():
    #if availability_values == None:
    #  load_saved_attributes()
    return city_values

def predict_house_price(city, area,location,bedroom, liftAvailable, Resale):
    #load_saved_attributes()
    try:
        loc_index = location_values.index(location)
        city_index = city_values.index(city)

    except:
        loc_index = -1
        city_index = -1


    loc_array = np.zeros(len(location_values))
    if loc_index >= 0:
        loc_array[loc_index] = 1

    city_array = np.zeros(len(city_values))
    if city_index >= 0:
        city_array[city_index] = 1

    city_array = city_array[:-1]
    loc_array = loc_array[:-1]
    sample = np.concatenate((np.array([area, bedroom, Resale,liftAvailable]),city_array, loc_array))

    return model.predict(sample.reshape(1,-1))[0]


if __name__ == '__main__':
    load_saved_attributes()
else:
    load_saved_attributes()
