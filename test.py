#Importing Packages
from skyfield.api import load, EarthSatellite, wgs84

#Defining Class TLE
class TLE:
    def __init__(self, file_name):
        self.tle_file_name = file_name
        return
    def __enter__(self):
        with open(self.tle_file_name, "r") as self.tle_file:
            self.tle_file_contents_list = self.tle_file.read().splitlines()
            self.sat_name = self.tle_file_contents_list[0]
            self.line1 = self.tle_file_contents_list[1]
            self.line2 = self.tle_file_contents_list[2]
        return self
    #Defining Exit Function for Exception Handling
    def __exit__(self, *args):
        if args == (None, None, None):
            print(f"Algorithm Completed Successfully for {self.sat_name}")
        return

#SGP4 Propagation Algorithm Using With Statement and TLE as context manager
with TLE("TLE files/TLE DS-EO 20240407 Spacetrack.txt") as tle_original:
    print(f'{tle_original.sat_name} File Parsed\nStarting Algorithm for {tle_original.sat_name}')
    #Creating skyfield EarthSatellite object for TLE
    ts = load.timescale()
    satellite = EarthSatellite(tle_original.line1, tle_original.line2, tle_original.sat_name, ts)
    print(satellite)
    #AOS LOS Event Contact Locator
    gsc_stn = wgs84.latlon(+1.29214, +103.78182)
    t0 = ts.utc(2024, 4, 8)
    t1 = ts.utc(2024, 4, 9)
    t, events = satellite.find_events(gsc_stn, t0, t1, altitude_degrees=5)
    event_names = 'rise above 5°', 'culminate', 'set below 5°'
    for ti, event in zip(t, events):
        name = event_names[event]
        print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)