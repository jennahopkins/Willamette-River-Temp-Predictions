# Build feature variables to be used in analysis and modeling.

# CONSTANTS
CLEAN_DATA_PATH = "data/cleaned/"
SAVE_PATH = "data/features/"

# LIBRARIES
import pandas as pd

# IMPORT DATA
meteo_data = pd.read_csv(f"{CLEAN_DATA_PATH}meteo_data.csv")
keizer_temp = pd.read_csv(f"{CLEAN_DATA_PATH}Keizer_temp.csv")
salem_discharge = pd.read_csv(f"{CLEAN_DATA_PATH}Salem_discharge.csv")
newberg_temp = pd.read_csv(f"{CLEAN_DATA_PATH}Newberg_temp.csv")
newberg_discharge = pd.read_csv(f"{CLEAN_DATA_PATH}Newberg_discharge.csv")

# MERGE DATA
salem_keizer_data = pd.merge(salem_discharge, keizer_temp, on = "date", how = "inner")
newberg_data = pd.merge(newberg_discharge, newberg_temp, on = "date", how = "inner")
water_data = pd.merge(salem_keizer_data, newberg_data, on = "date", how = "inner")
features_data = pd.merge(meteo_data, water_data, on = "date", how = "inner")

#print(features_data.shape[0]) # should be 369
features_data = features_data.sort_values("date").reset_index(drop=True) # sort by date and reset index
features_data["date"] = pd.to_datetime(features_data["date"])


# CREATE LAG AND ROLLING FEATURES
groups = []
for year, group in features_data.groupby(features_data["date"].dt.year):
    group = group.copy()

    # create lag target water features
    group["target_watertemp_max_lag1"] = group["target_max_watertemp"].shift(1)
    group["target_watertemp_max_lag2"] = group["target_max_watertemp"].shift(2)
    group["target_watertemp_max_lag3"] = group["target_max_watertemp"].shift(3)
    group["target_watertemp_mean_lag1"] = group["target_mean_watertemp"].shift(1)
    group["target_watertemp_mean_lag2"] = group["target_mean_watertemp"].shift(2)
    group["target_watertemp_mean_lag3"] = group["target_mean_watertemp"].shift(3)
    group["target_discharge_lag1"] = group["target_discharge"].shift(1)
    group["target_discharge_lag2"] = group["target_discharge"].shift(2)
    group["target_discharge_lag3"] = group["target_discharge"].shift(3)

    group["target_watertemp_max_roll3"] = group["target_max_watertemp"].shift(1).rolling(3).mean()
    group["target_watertemp_mean_roll3"] = group["target_mean_watertemp"].shift(1).rolling(3).mean()
    group["target_discharge_roll3"] = group["target_discharge"].shift(1).rolling(3).mean()
    # create lag upstream water features
    group["upstream_watertemp_max_lag1"] = group["upstream_max_watertemp"].shift(1)
    group["upstream_watertemp_max_lag2"] = group["upstream_max_watertemp"].shift(2)
    group["upstream_watertemp_max_lag3"] = group["upstream_max_watertemp"].shift(3)
    group["upstream_watertemp_mean_lag1"] = group["upstream_mean_watertemp"].shift(1)
    group["upstream_watertemp_mean_lag2"] = group["upstream_mean_watertemp"].shift(2)
    group["upstream_watertemp_mean_lag3"] = group["upstream_mean_watertemp"].shift(3)
    group["upstream_discharge_lag1"] = group["upstream_discharge"].shift(1)
    group["upstream_discharge_lag2"] = group["upstream_discharge"].shift(2)
    group["upstream_discharge_lag3"] = group["upstream_discharge"].shift(3)

    group["upstream_watertemp_max_roll3"] = group["upstream_max_watertemp"].shift(1).rolling(3).mean()
    group["upstream_watertemp_mean_roll3"] = group["upstream_mean_watertemp"].shift(1).rolling(3).mean()
    group["upstream_discharge_roll3"] = group["upstream_discharge"].shift(1).rolling(3).mean()
    # create lag air temperature features
    group["max_airtemp_lag1"] = group["max_airtemp_f"].shift(1)
    group["max_airtemp_lag2"] = group["max_airtemp_f"].shift(2)
    group["max_airtemp_lag3"] = group["max_airtemp_f"].shift(3)
    group["min_airtemp_lag1"] = group["min_airtemp_f"].shift(1)
    group["min_airtemp_lag2"] = group["min_airtemp_f"].shift(2)
    group["min_airtemp_lag3"] = group["min_airtemp_f"].shift(3)
    group["mean_airtemp_lag1"] = group["mean_airtemp_f"].shift(1)
    group["mean_airtemp_lag2"] = group["mean_airtemp_f"].shift(2)
    group["mean_airtemp_lag3"] = group["mean_airtemp_f"].shift(3)
    group["dewpoint_lag1"] = group["dewpoint_2m_max"].shift(1)
    group["dewpoint_lag2"] = group["dewpoint_2m_max"].shift(2)
    group["dewpoint_lag3"] = group["dewpoint_2m_max"].shift(3)

    group["max_airtemp_roll3"] = group["max_airtemp_f"].shift(1).rolling(3).mean()
    group["min_airtemp_roll3"] = group["min_airtemp_f"].shift(1).rolling(3).mean()
    group["mean_airtemp_roll3"] = group["mean_airtemp_f"].shift(1).rolling(3).mean()
    group["dewpoint_roll3"] = group["dewpoint_2m_max"].shift(1).rolling(3).mean()

    groups.append(group)

features_data = pd.concat(groups).reset_index(drop=True)

# CREATE SEASON PROGRESS VARIABLE
date_series = pd.to_datetime(features_data["date"])
june1 = pd.to_datetime(date_series.dt.year.astype(str) + "-06-01")
features_data["days_since_june1"] = (date_series - june1).dt.days

# DROP NAs FROM LAGGED VARIABLES
features_data = features_data.dropna()
#print(features_data.shape[0]) # should be 356

# ADD TARGET COLUMNS
features_data["target_1d"] = features_data["target_max_watertemp"].shift(-1)
features_data["target_3d"] = features_data["target_max_watertemp"].shift(-3)
features_data["target_5d"] = features_data["target_max_watertemp"].shift(-5)
features_data["target_7d"] = features_data["target_max_watertemp"].shift(-7)
features_data["target_10d"] = features_data["target_max_watertemp"].shift(-10)
features_data["above_72f_1d"] = (features_data["target_1d"] > 72).astype(int)
features_data["above_72f_3d"] = (features_data["target_3d"] > 72).astype(int)
features_data["above_72f_5d"] = (features_data["target_5d"] > 72).astype(int)
features_data["above_72f_7d"] = (features_data["target_7d"] > 72).astype(int)
features_data["above_72f_10d"] = (features_data["target_10d"] > 72).astype(int)

# DROP NAs FROM TARGET VARIABLES
features_data = features_data.dropna()
#print(features_data.shape[0]) # should be 346



# SAVE DATA
features_data.to_csv(f"{SAVE_PATH}features_data.csv", index=False)