from django.shortcuts import render
from django.http import HttpResponse
from tensorflow import keras
import joblib
import dateparser
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


def index(request):
    return render(request, 'api.html')


@csrf_exempt
def predict(request):
    # MODEL_PATH = 'models/TFAuto'
    # model = keras.models.load_model(MODEL_PATH)
    # scaler = joblib.load(MODEL_PATH + '/TFScaler.pkl')

    model = joblib.load('models/RandomForestRegressor')
    scaler = joblib.load('models/RFScaler')

    bouwjaar = 0.
    kilometer_stand = 0.
    vermogen = 0.
    is_handgeschakeld = 0.
    is_benzine = 0.
    upload_datum = 0.
    apk = 0.

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
            upload_datum = float(datetime.now().toordinal() - dateparser.parse(value).toordinal())
        if "apk" in key:
            apk = float(datetime.now().toordinal() - dateparser.parse(value).toordinal())

    #try:
    row = [bouwjaar, kilometer_stand, vermogen, is_handgeschakeld, is_benzine, upload_datum, apk]
    autos_scaled = scaler.transform([row])
    prediction = int(model.predict(autos_scaled)[0])
    #except Exception as e:
        #return HttpResponse(json.dumps({'error': str(e)}))

    return HttpResponse(json.dumps({'prediction': prediction}))
