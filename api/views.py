from django.http import HttpResponse
import joblib
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd


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

    #try:
    target_names = ["bouwjaar", "kilometer_stand", "vermogen", "is_handgeschakeld", "is_benzine", "titel"]
    row = pd.DataFrame([[bouwjaar, kilometer_stand, vermogen, is_handgeschakeld, is_benzine, titel]], columns=target_names)
    prediction = int(model.predict(row)[0])
    #except Exception as e:
        #return HttpResponse(json.dumps({'error': str(e)}))

    return HttpResponse(json.dumps({'prediction': prediction}))
