from django.shortcuts import render
from django.http import HttpResponse
from tensorflow import keras
import joblib
import dateparser
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import pandas as pd


def index(request):
    return render(request, 'api.html')


@csrf_exempt
def predict(request):
    model = joblib.load('models/Regressor')
    # tensorflowModel = keras.models.load_model('models/NeuralNetwork')

    titel = ""
    bouwjaar = 0.
    kilometer_stand = 0.
    vermogen = 0.
    is_handgeschakeld = 0.
    is_benzine = 0.
    upload_datum = 0.
    apk = 0.

    for key, value in json.loads(request.body.decode("utf-8")).items():
        if "titel" in key:
            titel = str(value)
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
    target_names = ["bouwjaar", "kilometer_stand", "vermogen", "is_handgeschakeld", "is_benzine",
                    "upload_datum", "apk", "titel"]
    row = pd.DataFrame([[bouwjaar, kilometer_stand, vermogen, is_handgeschakeld, is_benzine, upload_datum, apk, titel]], columns=target_names)
    prediction = int(model.predict(row)[0])
    #except Exception as e:
        #return HttpResponse(json.dumps({'error': str(e)}))

    return HttpResponse(json.dumps({'prediction': prediction}))
