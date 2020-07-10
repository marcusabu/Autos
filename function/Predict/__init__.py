import logging

import azure.functions as func
import joblib
import pandas as pd
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        titel = str(req.params.get('titel'))
        kilometer_stand = int(req.params.get('kilometer_stand'))
        is_handgeschakeld = bool(req.params.get('is_handgeschakeld'))
        bouwjaar = int(req.params.get('bouwjaar'))
        is_benzine = bool(req.params.get('is_benzine'))
        vermogen = int(req.params.get('vermogen'))

        model = joblib.load('Regressor')

        target_names = ["bouwjaar", "kilometer_stand", "vermogen",
                        "is_handgeschakeld", "is_benzine", "titel"]

        row = pd.DataFrame([[bouwjaar, kilometer_stand, vermogen,
                             is_handgeschakeld, is_benzine, titel]], columns=target_names)
        prediction = int(model.predict(row)[0])

        return func.HttpResponse(json.dumps({'prediction': prediction}))
    except Exception as e:
        return func.HttpResponse(str(e))
