import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import pandas as pd
import requests
from kaggle.api.kaggle_api_extended import KaggleApi

# Configure Kaggle API
api = KaggleApi()
api.authenticate()

# Specify the dataset name
DATASET_NAME = "rsna-breast-cancer-detection"  # Change to your dataset

# Specify the folders you want to download
FOLDERS_TO_DOWNLOAD = ["train_images/10006", "train_images/10011"]  # Add your folder names

# Specify the local download directory
DOWNLOAD_DIR = "/Users/ostapbodnar/Desktop/NULP/магрістратура/1 семестр/ml/data"  # Change to your desired local directory

files = pd.read_csv("file_names.csv", header=0, index_col=0)


def load_file(patient_image):
    try:
        patient, image = patient_image
        if os.path.exists("data/" + str(image) + '.dcm') and False:
            return
        name = str(patient) + "/" + str(image) + '.dcm'
        api.competition_download_file(DATASET_NAME, "train_images/" + name, quiet=True)

        file_name = str(image) + '.dcm'
        if os.path.exists(file_name):
            shutil.move(file_name, "data")
        else:
            with zipfile.ZipFile(file_name + '.zip', 'r') as zip_ref:
                zip_ref.extractall(DOWNLOAD_DIR)
            print('loaded - ', file_name)
            os.remove(file_name + '.zip')
    except Exception as error:
        if "TooManyRequests" in str(error):
            print("sleeping for 15 minutes")
            sleep(60 * 15)
            load_file(patient_image)
            return
        print(error)
        print(patient_image, "- FAILED")


def load_file_from_url(patient_image):
    print(patient_image)
    try:
        patient, image = patient_image
        if os.path.exists("data/" + str(image) + '.dcm') and False:
            return
        file_name = str(image) + '.dcm'
        if os.path.exists(file_name):
            shutil.move(file_name, "data")
        url = f"https://www.kaggle.com/competitions/rsna-breast-cancer-detection/download/V2TqRvICQboZzyYXLLIi%2Fversions%2FU0SO15qTDXIAlfqZRbmU%2Fdirectories%2Ftrain_images%2Fdirectories%2F{patient}%2Ffiles%2F{image}.dcm?datasetVersionNumber=undefined"
        response = requests.get(url, allow_redirects=True, stream=True,
                                headers={
                                    "Cookie": "_ga_T7QHS60L4Q=GS1.1.1697296207.17.1.1697296759.0.0.0; _ga=GA1.1.1603882064.1693030644; GCLB=CK71mpGekIbQbQ; CSRF-TOKEN=CfDJ8GzjVQ-Raa5Ckq3ov4atXHBBqFtPGeWRisT5xgh2l_7iYFJLDa3uGm_tkkIv5KZJv4Z2yM4aqModDLhhPLZC9l5OUY81lTbAtzCuzSaGZg; XSRF-TOKEN=CfDJ8MNDZicIIV1FkFqrIKA-ArGyhz1GXQbO_JRLQ20nngIG0Fblh6WqqGZjLfBHcaPf95KbpiSw9qNw6XEgNsvMvc-gBFuE73h--LLVNIIGhbzckwdz0XISRyI2ErrW9UjXbe82Pk0UY4v4SJ6hTJMRBHg; CLIENT-TOKEN=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpc3MiOiJrYWdnbGUiLCJhdWQiOiJjbGllbnQiLCJzdWIiOiJvc3RhcGJvZG5hciIsIm5idCI6IjIwMjMtMTAtMTRUMTU6MTk6MDQuMDQ4OTU1OVoiLCJpYXQiOiIyMDIzLTEwLTE0VDE1OjE5OjA0LjA0ODk1NTlaIiwianRpIjoiMDliYmE1NzAtZDU3NC00OTAzLTg2MTktZDFlMGVkNmJhZDYzIiwiZXhwIjoiMjAyMy0xMS0xNFQxNToxOTowNC4wNDg5NTU5WiIsInVpZCI6Njc0MjMyMCwiZGlzcGxheU5hbWUiOiJPc3RhcCBCb2RuYXIiLCJlbWFpbCI6Im9zdGFwYm9kNjc0QGdtYWlsLmNvbSIsInRpZXIiOiJOb3ZpY2UiLCJ2ZXJpZmllZCI6dHJ1ZSwicHJvZmlsZVVybCI6Ii9vc3RhcGJvZG5hciIsInRodW1ibmFpbFVybCI6Imh0dHBzOi8vc3RvcmFnZS5nb29nbGVhcGlzLmNvbS9rYWdnbGUtYXZhdGFycy90aHVtYm5haWxzL2RlZmF1bHQtdGh1bWIucG5nIiwiZmYiOlsiS2VybmVsc0RyYWZ0VXBsb2FkQmxvYiIsIktlcm5lbHNGaXJlYmFzZUxvbmdQb2xsaW5nIiwiQ29tbXVuaXR5TG93ZXJIZWFkZXJTaXplcyIsIkNvbXBldGl0aW9uc0ZpbGVzRHJvcEthZ2dsZUFwaSIsIkFsbG93Rm9ydW1BdHRhY2htZW50cyIsIktlcm5lbHNTYXZlQ2VsbE91dHB1dCIsIkZyb250ZW5kRXJyb3JSZXBvcnRpbmciLCJEYXRhc2V0c01hbmFnZWRGb2N1c09uT3BlbiIsIkNoYW5nZURhdGFzZXRPd25lcnNoaXBUb09yZyIsIk1hdVJlcG9ydCIsIk1vZGVsc0NhY2hlZFRhZ1NlcnZpY2VFbmFibGVkIiwiTW9kZWxzVGFiT25Db21wZXRpdGlvblBhZ2UiLCJEYXRhc2V0c1NoYXJlZFdpdGhUaGVtU2VhcmNoIiwiRGF0YXNldHNWb3RpbmdDaGlwcyIsIk1vZGVsSW5zdGFuY2VSZW5kZXJlZFVzYWdlIiwiUmVjZW50bHlWaWV3ZWRNb2RlbHNTaGVsZiIsIk1vZGVsc09wZW5WZXJ0ZXgiLCJEYXRhc2V0c0ZlZWRiYWNrc0ZpbHRlcnMiXSwiZmZkIjp7Iktlcm5lbEVkaXRvckF1dG9zYXZlVGhyb3R0bGVNcyI6IjMwMDAwIiwiRnJvbnRlbmRFcnJvclJlcG9ydGluZ1NhbXBsZVJhdGUiOiIwIiwiRW1lcmdlbmN5QWxlcnRCYW5uZXIiOiJ7IH0iLCJDbGllbnRScGNSYXRlTGltaXQiOiI0MCIsIkZlYXR1cmVkQ29tbXVuaXR5Q29tcGV0aXRpb25zIjoiNjAwOTUsNTQwMDAsNTcxNjMiLCJBZGRGZWF0dXJlRmxhZ3NUb1BhZ2VMb2FkVGFnIjoiZGlzYWJsZWQiLCJTaW1Db21wZXRpdGlvbklkc1RvSWdub3JlVXBsb2FkTGltaXQiOiI2MDI0Myw2MTI1MCIsIkNvbXBldGl0aW9uTWV0cmljVGltZW91dE1pbnV0ZXMiOiIzMCIsIkNvbXBldGl0aW9uSWRzUmVxdWlyaW5nVXNlclZlcmlmaWNhdGlvbiI6IjU5NDI4LDYyMzkwIn0sInBpZCI6ImthZ2dsZS0xNjE2MDciLCJzdmMiOiJ3ZWItZmUiLCJzZGFrIjoiQUl6YVN5QTRlTnFVZFJSc2tKc0NaV1Z6LXFMNjU1WGE1SkVNcmVFIiwiYmxkIjoiYWFmNmUxN2M1OTQ2OGVkMjllMWQ0OWQ2ZGExNmY4MWEyNjZiYmJjMSJ9.; ka_sessionid=6dd3ec99ff4968ba9abbaec89008b494; __Host-KAGGLEID=CfDJ8MNDZicIIV1FkFqrIKA-ArFvSXQdFfaAjWyGX8Tol7v1UGDYmuQVVO_W8AkomsQ9zvxQmr34eEeps4od592Xf_8UAAMARdGJG1aoO_zRl_OJTjGdNivUmtVp",
                                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0"})

        with open(file_name + ".zip", 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile(file_name + '.zip', 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

        os.remove(file_name + '.zip')
    except Exception as error:
        print(error)
        print(patient_image, "- FAILED")
    print(patient_image, " - DONE")


with ThreadPoolExecutor() as executor:
    executor.map(load_file_from_url, files.to_numpy())
