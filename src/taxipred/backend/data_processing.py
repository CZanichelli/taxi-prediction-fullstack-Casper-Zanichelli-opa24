from taxipred.utils.constants import ORIGINAL_DATA_FILE
import pandas as pd
import json


TRAFFIC_ENCODING_MAP = {
    "LÅG": 2,
    "MEDEL": 1,
    "HÖG": 0

}


class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(ORIGINAL_DATA_FILE)

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))
