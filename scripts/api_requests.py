# Access APIs to retrieve data for the application


# CONSTANTS
TARGET_STN_NUM = "14197900"
TARGET_STN_NAME = "Newberg"
UPSTREAM_TEMP_NUM = "14192015"
UPSTREAM_TEMP_NAME = "Keizer"
UPSTREAM_DISCHARGE_NUM = "14191000"
UPSTREAM_DISCHARGE_NAME = "Salem"

START_DATE = "2022-06-01"
END_DATE = "2026-06-01"

TARGET_COORDS = (45.2845625, -122.9614893)

USGS_URL = "https://waterservices.usgs.gov/nwis/dv/"
METEO_URL = "https://archive-api.open-meteo.com/v1/archive/"

SAVE_PATH = "data/raw/"

# LIBRARIES
import requests
import pandas as pd

# FUNCTIONS
def get_usgs_temp_data(station_number, start_date, end_date, parameter_code, filename, max_id = 0, min_id = 2, values_id = 0):
    """
    Retrieve data from the Daily Values USGS API for a given station number, date range, and parameter code.

    Args:
        station_number (str): The USGS station number.
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.
        parameter_code (str): The USGS parameter code for the desired data.
        filename (str): The name of the file to save the data to (without extension).
        max_id (int): The index of the time series for maximum readings in the API response.
        min_id (int): The index of the time series for mean readings in the API response
        values_id (int): The index of the values list in the API response.
    """
    url = f"{USGS_URL}?sites={station_number}&parameterCd={parameter_code}&startDT={start_date}&endDT={end_date}&format=json"
    response = requests.get(url)
    data = response.json()
    max_readings = data["value"]["timeSeries"][max_id]["values"][values_id]["value"]
    mean_readings = data["value"]["timeSeries"][min_id]["values"][values_id]["value"]

    df_max = pd.DataFrame(max_readings)
    df_mean = pd.DataFrame(mean_readings)

    df_max = df_max.rename(columns = {"value": "max_watertemp_c", "qualifiers": "qualifiers_max_watertemp"})
    df_mean =df_mean.rename(columns = {"value": "mean_watertemp_c", "qualifiers": "qualifiers_mean_watertemp"})

    df_merge = pd.merge(df_max, df_mean, on = "dateTime", how = "outer")

    df_merge.to_csv(f"{SAVE_PATH}{filename}.csv", index = False)

def get_usgs_discharge_data(station_number, start_date, end_date, parameter_code, filename, id = 0, values_id = 0):
    """
    Retrieve data from the Daily Values USGS API for a given station number, date range, and parameter code.

    Args:
        station_number (str): The USGS station number.
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.
        parameter_code (str): The USGS parameter code for the desired data.
        filename (str): The name of the file to save the data to (without extension).
        id (int): The index of the time series for readings in the API response.
        values_id (int): The index of the values list in the API response.
    """
    url = f"{USGS_URL}?sites={station_number}&parameterCd={parameter_code}&startDT={start_date}&endDT={end_date}&format=json"
    response = requests.get(url)
    data = response.json()
    readings = data["value"]["timeSeries"][id]["values"][values_id]["value"]

    df = pd.DataFrame(readings)

    df = df.rename(columns = {"value": "discharge", "qualifiers": "qualifiers_discharge"})

    df.to_csv(f"{SAVE_PATH}{filename}.csv", index = False)

def get_meteo_data(parameters, start_date, end_date, filename):
    """
    Retrieve data from the Daily Open Meteo API for a given station number, date range, and parameter code.

    Args:
        parameters (str): The parameters to retrieve from the API, separated by commas.
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.
        filename (str): The name of the file to save the data to (without extension).
    """
    url = f"{METEO_URL}?latitude={TARGET_COORDS[0]}&longitude={TARGET_COORDS[1]}&daily={parameters}&start_date={start_date}&end_date={end_date}&temperature_unit=fahrenheit&timezone=America%2FLos_Angeles"
    response = requests.get(url)
    data = response.json()
    readings = data["daily"]

    param_data_list = []
    for key in readings.keys():
        param_data_list.append(readings[key])

    rows = list(zip(*param_data_list))

    df = pd.DataFrame(rows, columns = readings.keys())

    df.to_csv(f"{SAVE_PATH}{filename}.csv", index = False)


# MAIN
if __name__ == "__main__":
    get_usgs_temp_data(TARGET_STN_NUM, START_DATE, END_DATE, "00010", f"{TARGET_STN_NAME}_temp")
    get_usgs_discharge_data(TARGET_STN_NUM, START_DATE, END_DATE, "00060", f"{TARGET_STN_NAME}_discharge")
    get_usgs_temp_data(UPSTREAM_TEMP_NUM, START_DATE, END_DATE, "00010", f"{UPSTREAM_TEMP_NAME}_temp", values_id = 1)
    get_usgs_discharge_data(UPSTREAM_DISCHARGE_NUM, START_DATE, END_DATE, "00060", f"{UPSTREAM_DISCHARGE_NAME}_discharge")

    get_meteo_data("temperature_2m_max,temperature_2m_min,temperature_2m_mean,dewpoint_2m_max", START_DATE, END_DATE, "meteo_data")