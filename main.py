import urllib.request
import gzip
import numpy as np

# base url to the meteostat hourly archive
BASE_URL = "https://open.meteostat.net/hourly/"

# station id that should be queried
STATION_ID = "10929" # konstanz, germany

# delta in pressure change over the last three hours (values taken from garmin instinct watch)
PRESSURE_DELTAS = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.0, 6.0]

# delta in average wind speeds from now to the next hour
WIND_DELTAS = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0]

def main():
    # download the historical data
    csv_data = list()
    fname, _ = urllib.request.urlretrieve(BASE_URL+STATION_ID+".csv.gz")
    with gzip.open(fname) as fd:
        for line in fd:
            line = line.decode("ascii").rstrip("\n")
            fields = line.split(",")
            if len(fields) == 14:
                csv_data.append(fields)

    # collect the data
    millibar_last_3h = list()
    wind_next_1h = list()
    for i in range(3, len(csv_data) - 1):
        try:
            mbar = float(csv_data[i-3][12]) - float(csv_data[i][12]) # decrease if storm is approaching
            wind = float(csv_data[i+1][8]) - float(csv_data[i][8]) # increase if storm is happening
            millibar_last_3h.append(mbar)
            wind_next_1h.append(wind)
        except:
            pass

    # convert to numpy
    millibar_last_3h = np.asarray(millibar_last_3h, dtype=np.float32)
    wind_next_1h = np.asarray(wind_next_1h, dtype=np.float32)

    # printout
    def f2s(x):
        return "%.1f" % (x)
    print("Pressure delta in 3h:\t%s" % ("\t\t".join(f2s(x) for x in PRESSURE_DELTAS)))
    print("                     \t%s" % ("\t\t".join(["fp/fn"] * len(PRESSURE_DELTAS))))

    # test all wind speeds
    for delta_w in WIND_DELTAS:
        # convert to a machine learning problem
        X = millibar_last_3h
        Y = (wind_next_1h > delta_w).astype(dtype=np.int32)

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
            all_errors.append("%s/%s" % (f2s(fp_rate),f2s(fn_rate)))
        
        # printout
        print("Wind %.1f km/h delta:\t%s" % (delta_w,"\t".join(all_errors)))


if __name__ == "__main__":
    main()