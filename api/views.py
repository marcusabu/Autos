from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
from tensorflow import keras
import joblib
import re
import dateparser
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'api.html')


@csrf_exempt
def predict(request):
    MODEL_PATH = 'models/TFAuto'
    model = keras.models.load_model(MODEL_PATH)
    scaler = joblib.load(MODEL_PATH + '/TFScaler.pkl')

    for key, value in json.loads(request.body.decode("utf-8")).items():
        if "kilometer_stand" in key:
            kilometer_stand = float(value)
        if "is_handgeschakeld" in key:
            is_handgeschakeld = float(value)
        if "bouwjaar" in key:
            bouwjaar = float(value)
        if "is_benzine" in key:
            is_benzine = float(value)
        if "vermogen" in key:
            vermogen = float(value)
        if "upload_datum" in key:
            timestamp = float(dateparser.parse(value).toordinal())

    try:
        row = [bouwjaar, kilometer_stand, vermogen, is_handgeschakeld, is_benzine, timestamp]
        autos_scaled = scaler.transform([row])
        prediction = int(model.predict(autos_scaled)[0][0])
    except Exception as e:
        return HttpResponse(str(e))

    return HttpResponse(json.dumps({'prediction': prediction}))
