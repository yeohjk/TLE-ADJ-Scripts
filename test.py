#Importing Packages
from skyfield.api import load, EarthSatellite, wgs84

#class TLE Refinement Manager
class TLE_Refinement_Manager:
    def __init__(self):
        self.file_dict = {"TLE":self.TLE_File_Propagator, "ANG":self.ANG_File_Propagator}
        self.file_type = input("Input File Type (TLE/ANG)\n")
        self.file_name = input("Input File Name with Extension\n")
        self.file_propagator = self.file_dict[self.file_type]
        self.file_propagator()
        return
    def TLE_File_Propagator(self):
        #Create TLE File object
        self.tle_file = TLE_File(f"TLE files/{self.file_name}")
        #Pass TLE File object to Propagator object
        ts = load.timescale()
        t = ts.utc(2024, 4, 8, 22, 45, 0)
        self.propagator_object = Propagator(self.tle_file.TLE_object, t, ts)
        return
    def ANG_File_Propagator(self):
        #Create ANG File object
        self.ang_file = ANG_File(f"Angle files/{self.file_name}")
        #Pass ANG File object to Propagator object
        ts = load.timescale()
        t = ts.utc(2024, 4, 20, 22, 45, 0)
        self.propagator_object = Propagator(self.ang_file.TLE_object, t, ts)
        return

#Defining Class Input File
class Input_File:
    def __init__(self, file_name):
        self.file_name = file_name
        self.exception = []
        self.file_load()
        self.parsing_TLE_info()
        return
    def file_load(self):
        print(f"\nLoading {self.file_name} into program")
        #Exception Handling
        try:
            self.loaded_file = open(self.file_name, "r")
            self.file_contents_list = self.loaded_file.read().splitlines()
            for line in self.file_contents_list:
                print(line)
        except:
            self.exception.append("Error with file loading into program")
        else:
            print(f"Loaded {self.file_name} into program")
        finally:
            self.loaded_file.close()
        return

#Defining Class TLE
class TLE_File(Input_File):
    def parsing_TLE_info(self):
        print("\nParsing TLE File")
        self.TLE_object = TLE(self.file_contents_list)
        print(f"TLE file for {self.TLE_object.sat_name} successfully parsed in program")
        return

#Defining Angle_File
class ANG_File(Input_File):
    def parsing_TLE_info(self):
        print("\nParsing Angle File")
        self.TLE_object = TLE(self.file_contents_list)
        print(f"Angle file for Sat Cat Number {self.TLE_object.sat_name} successfully parsed in program")
        return

#Defining Class TLE
class TLE:
    def __init__(self, file_contents_list):
        self.sat_name = file_contents_list[0][0:5]
        self.line1 = file_contents_list[1]
        self.line2 = file_contents_list[2]
        return

#Defining Class Propagator
class Propagator:
    def __init__(self, tle_object, time_stamp, ts):     
        #Creating skyfield Ground Station and EarthSatellite object for TLE
        self.tle_object = tle_object
        self.time_stamp = time_stamp
        self.ts = ts
        self.gnd_stn = wgs84.latlon(+1.29214, +103.78182, elevation_m=83)
        self.satellite = EarthSatellite(self.tle_object.line1, self.tle_object.line2, self.tle_object.sat_name, self.ts)
        print(self.satellite)
        #SGP4 Propagation Algorithm with Exception Handling
        try:
            print(f'\nStarting SGP4 Propagation for {self.tle_object.sat_name}')
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
            print(f'Completed SGP4 Propagation for {self.tle_object.sat_name}')
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
    
#Defining class Refined_TLE
class Refined_TLE:
    def __init__(self):
        return

Manager_Inst = TLE_Refinement_Manager()