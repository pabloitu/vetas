from io import BytesIO
import urllib.request
import pandas as pd
import datetime as dt


def download_catalog_sed(
        starttime=dt.datetime(1970, 1, 1),
        endtime=dt.datetime.now(),
        minmagnitude=0.01,
        delta_m=0.1,
):
    print('downloading data..\n')

    basequery = 'http://arclink.ethz.ch/fdsnws/event/1/query?'
    sttm = 'starttime=' + starttime.strftime("%Y-%m-%dT%H:%M:%S")
    endtm = '&endtime=' + endtime.strftime("%Y-%m-%dT%H:%M:%S")
    minmag = '&minmagnitude=' + str(minmagnitude - delta_m / 2)

    link = basequery + sttm + endtm + minmag + '&format=text'
    response = urllib.request.urlopen(link)
    data = response.read()

    df = pd.read_csv(BytesIO(data), delimiter="|")

    df.rename(
        {
            "Magnitude": "magnitude",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Time": "time",
            "Depth/km": "depth"
        }, axis=1, inplace=True)

    df["time"] = pd.to_datetime(df["time"])
    df.sort_values(by="time", inplace=True)

    return df
