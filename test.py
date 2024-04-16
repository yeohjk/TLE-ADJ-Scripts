#Importing Packages
from skyfield.api import load, EarthSatellite, wgs84

#class TLE Refinement Manager
class TLE_Refinement_Manager:
    def __init__(self, tle_file_name):
        self.tle_file_name = tle_file_name
        #Create TLE Object
        self.tle_object = TLE(f"TLE files/{self.tle_file_name}")
        #Pass TLE object to Propagator Object
        ts = load.timescale()
        t = ts.utc(2024, 4, 8, 22, 45, 0)
        self.propagator_object = Propagator(self.tle_object, t, ts)
        return

#Defining Class TLE
class TLE:
    def __init__(self, tle_file_name):
        self.tle_file_name = tle_file_name
        print("Creating TLE Object")
        self.file_load()
        return
    def file_load(self):
        #Exception Handling
        try: 
            self.tle_file = open(self.tle_file_name, "r")   
        except:
            raise Exception("TLE file loading error. Check TLE file name and TLE file content format") 
        else:
            self.tle_file_contents_list = self.tle_file.read().splitlines()
            self.sat_name = self.tle_file_contents_list[0]
            self.line1 = self.tle_file_contents_list[1]
            self.line2 = self.tle_file_contents_list[2]
            print(f"{self.sat_name} TLE file successfully loaded into program\nTLE Object created successfully for {self.sat_name}")
        finally:
            self.tle_file.close()
        return

#Defining Angle_File
class Angle_File:
    def __init__(self):
        return

#Defining Class Propagator
class Propagator:
    def __init__(self, tle_object = 0, time_stamp = 0, ts = 0):     
        #Creating skyfield Ground Station and EarthSatellite object for TLE
        self.ts = ts
        self.time_stamp = time_stamp
        self.gnd_stn = wgs84.latlon(+1.29214, +103.78182, elevation_m=83)
        self.satellite = EarthSatellite(tle_object.line1, tle_object.line2, tle_object.sat_name, self.ts)
        print(self.satellite)
        #SGP4 Propagation Algorithm with Exception Handling
        try:
            print(f'Starting SGP4 Propagation for {tle_object.sat_name}')
            #Satellite Az Al Position at time t
            self.difference_vec_func = self.satellite - self.gnd_stn
            self.topocentric_pos_vec = self.difference_vec_func.at(self.time_stamp)
            self.sat_el, self.sat_az, self.sat_distance = self.topocentric_pos_vec.altaz()
            print(f"Elevation Angle = {self.sat_el.degrees}")
            print(f"Azimuth Angle = {self.sat_az.degrees}")
            print(f"Distance (km) = {self.sat_distance.km}")
        except:
            raise Exception("SGP4 Propagation Error.") 
        else:
            print(f'Completed SGP4 Propagation for {tle_object.sat_name}')
        return 
    def AOS_LOS_Locator(self, t0, t1, min_elev):
        #AOS LOS Event Contact Locator
        t0 = self.ts.utc(2024, 4, 8)
        t1 = self.ts.utc(2024, 4, 9)
        min_elev = 5
        list_times, event_flags = self.satellite.find_events(self.gnd_stn, t0, t1, altitude_degrees=min_elev)
        event_names = 'rise above 5°', 'culminate', 'set below 5°'
        for ti, event in zip(list_times, event_flags):
            name = event_names[event]
            print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
        return
    
#Defining Refined_TLE
class Refined_TLE:
    def __init__(self):
        return
    
TLE_Refinement_Manager("TLE DS-EO 20240407 Spacetrack.txt")