import urllib.request
import gzip
import numpy as np
import argparse

# base url to the meteostat hourly archive
BASE_URL = "https://open.meteostat.net/hourly/"

# delta in pressure change over the last three hours (values taken from garmin instinct watch)
PRESSURE_DELTAS = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.0, 6.0]

# delta in average wind speeds from now to the next hour
WIND_DELTAS = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0]

def float2string(x):
    return "%.1f" % (x)

def safe_string2float(x):
    res = -1.0
    try:
        res = float(x)
    except:
        pass
    return res

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Evaluate the storm alert feature of the Garmin Instinct watch.")
    parser.add_argument("--forecast", type=int, default=1, required=False, help="Time horizon for weather forecasting in hours.")
    parser.add_argument("--station", type=str, default="10929", required=False, help="Station ID for which to do the weather forecast.")
    args = parser.parse_args()

    # download the historical data
    csv_data = list()
    fname, _ = urllib.request.urlretrieve(BASE_URL+args.station+".csv.gz")
    with gzip.open(fname) as fd:
        for line in fd:
            line = line.decode("ascii").rstrip("\n")
            fields = line.split(",")
            if len(fields) == 14:
                csv_data.append(fields)
    assert len(csv_data) > 0

    # collect the data
    pressure_change_3h = list()
    wind_forecast = list()
    for i in range(3, len(csv_data)-args.forecast):
        delta_p = None
        delta_w = None
        try:
            delta_p = float(csv_data[i-3][12]) - float(csv_data[i][12]) # decrease if storm is approaching
            max_wind = max([safe_string2float(x[8]) for x in csv_data[i+1:i+args.forecast+1]])
            if max_wind > 0.0:
                delta_w = max_wind - float(csv_data[i][8]) # increase if storm is happening
        except:
            pass
        if not delta_p is None and not delta_w is None:
            pressure_change_3h.append(delta_p)
            wind_forecast.append(delta_w)
    assert len(pressure_change_3h) > 0 and len(pressure_change_3h) == len(wind_forecast)

    # convert to numpy
    pressure_change_3h = np.asarray(pressure_change_3h, dtype=np.float32)
    wind_forecast = np.asarray(wind_forecast, dtype=np.float32)

    # printout
    print("Pressure delta in 3h:\t%s" % ("\t\t".join(float2string(x) for x in PRESSURE_DELTAS)))
    print("                     \t%s" % ("\t\t".join(["fp/fn"] * len(PRESSURE_DELTAS))))

    # test all wind speeds
    for delta_w in WIND_DELTAS:
        # convert to a machine learning problem
        X = pressure_change_3h
        Y = (wind_forecast > delta_w).astype(dtype=np.int32)

        # store the error rates
        all_errors = list()

        # try to predict using the rates as thresholds
        for delta_p in PRESSURE_DELTAS:
            # prediction
            Y_hat = (X > delta_p).astype(dtype=np.int32)

            # error rates
            error = Y - Y_hat
            false_positives = (error < 0).astype(dtype=np.int32)
            false_negatives = (error > 0).astype(dtype=np.int32)
            fp_rate = (np.sum(false_positives) / np.sum(Y_hat)) * 100.0
            fn_rate = (np.sum(false_negatives) / np.sum(1-Y_hat)) * 100.0
            
            # printout
            all_errors.append("%s/%s" % (float2string(fp_rate),float2string(fn_rate)))
        
        # printout
        print("Wind %.1f km/h delta:\t%s" % (delta_w,"\t".join(all_errors)))


if __name__ == "__main__":
    main()