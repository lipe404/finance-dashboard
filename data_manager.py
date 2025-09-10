import json
import pandas as pd
from datetime import datetime
import os


class DataManager:
    def __init__(self, date_file='finance_data.json'):
        self.data_file = data_file
        self.data = self.load_data()