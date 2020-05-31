from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
from tensorflow import keras
import joblib
import re
import dateparser
import numpy as np


def predict(request):
    MODEL_PATH = 'models/TFAuto'
    model = keras.models.load_model(MODEL_PATH)
    scaler = joblib.load(MODEL_PATH + '/TFScaler.pkl')

    for key, value in request.GET.items():
        if "kilometer_stand" in key:
            kilometer_stand = float(re.sub("[^0-9]", "", value))
        if "transmissie" in key:
            isHandgeschakeld = float(bool("Handgeschakeld" in value))
        if "bouwjaar" in key:
            bouwjaar = float(value)
        if "brandstof" in key:
            isBenzine = float(bool("Benzine" in value))
        if "vermogen" in key:
            vermogen = float(re.sub("[^0-9]", "", value))
        if "upload_datum" in key:
            timestamp = float(dateparser.parse(value).toordinal())

    row = [bouwjaar, kilometer_stand, vermogen, isHandgeschakeld, isBenzine, timestamp]
    autos_scaled = scaler.transform([row])
    prediction = int(model.predict(autos_scaled)[0][0])

    return HttpResponse(prediction)
