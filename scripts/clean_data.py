# Clean data from the API requests to be later used for analysis and modeling.

# CONSTANTS
RAW_DATA_PATH = "data/raw/"
SAVE_PATH = "data/cleaned/"

# LIBRARIES
import pandas as pd

# LOAD DATA
meteo_data = pd.read_csv(f"{RAW_DATA_PATH}meteo_data.csv")
keizer_temp = pd.read_csv(f"{RAW_DATA_PATH}Keizer_temp.csv")
salem_discharge = pd.read_csv(f"{RAW_DATA_PATH}Salem_discharge.csv")
newberg_temp = pd.read_csv(f"{RAW_DATA_PATH}Newberg_temp.csv")
newberg_discharge = pd.read_csv(f"{RAW_DATA_PATH}Newberg_discharge.csv")

# CONVERT TIME COLUMNS TO DATETIME
meteo_data["time"] = pd.to_datetime(meteo_data["time"])
keizer_temp["dateTime"] = pd.to_datetime(keizer_temp["dateTime"])
salem_discharge["dateTime"] = pd.to_datetime(salem_discharge["dateTime"])
newberg_temp["dateTime"] = pd.to_datetime(newberg_temp["dateTime"])
newberg_discharge["dateTime"] = pd.to_datetime(newberg_discharge["dateTime"])

# FILTER SUMMER MONTHS
meteo_data = meteo_data[meteo_data["time"].dt.month.isin([6, 7, 8])]
keizer_temp = keizer_temp[keizer_temp["dateTime"].dt.month.isin([6, 7, 8])]
salem_discharge = salem_discharge[salem_discharge["dateTime"].dt.month.isin([6, 7, 8])]
newberg_temp = newberg_temp[newberg_temp["dateTime"].dt.month.isin([6, 7, 8])]
newberg_discharge = newberg_discharge[newberg_discharge["dateTime"].dt.month.isin([6, 7, 8])]

# RENAME AIR TEMPCOLUMNS
meteo_data = meteo_data.rename(columns = {"temperature_2m_max": "max_airtemp_f", "temperature_2m_min": "min_airtemp_f", "temperature_2m_mean": "mean_airtemp_f"})

# CONVERT TO NUMERIC
meteo_data["max_airtemp_f"] = pd.to_numeric(meteo_data["max_airtemp_f"], errors = "coerce")
meteo_data["min_airtemp_f"] = pd.to_numeric(meteo_data["min_airtemp_f"], errors = "coerce")
meteo_data["mean_airtemp_f"] = pd.to_numeric(meteo_data["mean_airtemp_f"], errors = "coerce")
keizer_temp["max_watertemp_c"] = pd.to_numeric(keizer_temp["max_watertemp_c"], errors = "coerce")
keizer_temp["mean_watertemp_c"] = pd.to_numeric(keizer_temp["mean_watertemp_c"], errors = "coerce")
salem_discharge["discharge"] = pd.to_numeric(salem_discharge["discharge"], errors = "coerce")
newberg_temp["max_watertemp_c"] = pd.to_numeric(newberg_temp["max_watertemp_c"], errors = "coerce")
newberg_temp["mean_watertemp_c"] = pd.to_numeric(newberg_temp["mean_watertemp_c"], errors = "coerce")
newberg_discharge["discharge"] = pd.to_numeric(newberg_discharge["discharge"], errors = "coerce")  

# CONVERT TO FAHRENHEIT
keizer_temp["max_watertemp_f"] = (keizer_temp["max_watertemp_c"] * 9/5) + 32
keizer_temp["mean_watertemp_f"] = (keizer_temp["mean_watertemp_c"] * 9/5) + 32
newberg_temp["max_watertemp_f"] = (newberg_temp["max_watertemp_c"] * 9/5) + 32
newberg_temp["mean_watertemp_f"] = (newberg_temp["mean_watertemp_c"] * 9/5) + 32

keizer_temp = keizer_temp.drop(columns = ["max_watertemp_c", "mean_watertemp_c"])
newberg_temp = newberg_temp.drop(columns = ["max_watertemp_c", "mean_watertemp_c"])

# STANDARDIZE DATE COLUMNS
meteo_data["date"] = meteo_data["time"].dt.date
meteo_data = meteo_data.drop(columns = ["time"])

keizer_temp["date"] = keizer_temp["dateTime"].dt.date
keizer_temp = keizer_temp.drop(columns = ["dateTime"])

salem_discharge["date"] = salem_discharge["dateTime"].dt.date
salem_discharge = salem_discharge.drop(columns = ["dateTime"])

newberg_temp["date"] = newberg_temp["dateTime"].dt.date
newberg_temp = newberg_temp.drop(columns = ["dateTime"])

newberg_discharge["date"] = newberg_discharge["dateTime"].dt.date
newberg_discharge = newberg_discharge.drop(columns = ["dateTime"])

# HANDLE MISSING DATA
#print(keizer_temp[keizer_temp["mean_watertemp_f"].isnull() == True])
keizer_temp = keizer_temp.sort_values("date").reset_index(drop = True)
keizer_temp["mean_watertemp_f"] = keizer_temp["mean_watertemp_f"].interpolate(method = "linear")
keizer_temp["qualifiers_mean_watertemp"] = keizer_temp["qualifiers_mean_watertemp"].fillna("['I']")

# RENAME UPSTREAM/TARGET COLUMNS
newberg_discharge = newberg_discharge.rename(columns = {"discharge": "target_discharge", "qualifiers_discharge": "qualifiers_target_discharge"})
newberg_temp = newberg_temp.rename(columns = {"max_watertemp_f": "target_max_watertemp", "mean_watertemp_f": "target_mean_watertemp", "qualifiers_max_watertemp": "qualifiers_target_max_watertemp", "qualifiers_mean_watertemp": "qualifiers_target_mean_watertemp"})
salem_discharge = salem_discharge.rename(columns = {"discharge": "upstream_discharge", "qualifiers_discharge": "qualifiers_upstream_discharge"})
keizer_temp = keizer_temp.rename(columns = {"max_watertemp_f": "upstream_max_watertemp", "mean_watertemp_f": "upstream_mean_watertemp", "qualifiers_max_watertemp": "qualifiers_upstream_max_watertemp", "qualifiers_mean_watertemp": "qualifiers_upstream_mean_watertemp"})


# SAVE CLEANED DATA
meteo_data.to_csv(f"{SAVE_PATH}meteo_data.csv", index = False)
keizer_temp.to_csv(f"{SAVE_PATH}Keizer_temp.csv", index = False)
salem_discharge.to_csv(f"{SAVE_PATH}Salem_discharge.csv", index = False)
newberg_temp.to_csv(f"{SAVE_PATH}Newberg_temp.csv", index = False)
newberg_discharge.to_csv(f"{SAVE_PATH}Newberg_discharge.csv", index = False)