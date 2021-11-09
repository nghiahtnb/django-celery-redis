import os.path

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
import json
import pandas as pd


@shared_task(bind=True,name="csv_processing")
def csv_processing(self, csvs, output_dir):
    progress_recorder = ProgressRecorder(self)
    for i in range(len(csvs)):
        filename = os.path.split(csvs[i])[-1]
        df = pd.read_excel(csvs[i])
        data = convert_json(df)
        json.dump(data, open(os.path.join(output_dir, filename.replace(".xlsx", ".json")), "w", encoding='utf-8-sig'))
        os.rename(csvs[i], os.path.join(output_dir, filename))
        progress_recorder.set_progress(i+1, len(csvs), description=f"Proccessing file {i}")
        time.sleep(1)


def convert_json(df):
    row = df.iloc[0]
    data = {
        "ORDER NO": row[0],
        "DELIVER TO": row[1],
        "STORE CODE": row[2] if not pd.isna(row[2]) else None,
        "Phone": row[3] if not pd.isna(row[3]) else None,
        "Fax": row[4] if not pd.isna(row[4]) else None,
        "Email": row[5] if not pd.isna(row[5]) else None,
        "Products": []
    }
    for index, row in df.iterrows():
        item = {
            "OUR CODE": str(row[6]),
            "YOUR CODE": row[7],
            "REQUIRED": row[8],
            "UNIT PRICE": row[9],
            "TOTAL": row[10],
            "DESCRIPTION": row[11],
            "BARCODE": str(row[12])
        }
        data["Products"].append(item)
    return data