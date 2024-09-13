import roller
from dbfunctions.dbinsert_roller import insert_roller
import pandas as pd
import json
import time

enheter = pd.read_csv('alle_enheter_110924', delimiter=',')

print(enheter['organisasjonsform.kode'].value_counts())
