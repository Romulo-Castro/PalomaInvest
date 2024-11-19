from app.models import model_ai as mAi
from flask import request
import json

class AiController:

    def getTese(self):
        pTicker = request.args.get('codigo')
        
        if pTicker:
            tese = mAi.getTese(pTicker.upper())
            return tese
        else:
            return json.dumps({"status": "error", "message": "Ticker não especificado."}, ensure_ascii=False)