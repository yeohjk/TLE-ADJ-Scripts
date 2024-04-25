#Importing Packages
from skyfield.api import load, EarthSatellite, wgs84
import os

#class TLE Refinement Manager
class TLE_Refinement_Manager:
    def __init__(self):
        #Assigning input file dictionaries
        self.tle_refinement_dict = {"Directory":"ANG files", "Content Class":TLE_ANG_Content, "Operation":self.TLE_Refinement_Process}
        self.tle_prop_dict = {"Directory":"TLE files", "Content Class":TLE_Content, "Operation":self.TLE_Propagation}
        #Assigning operation mode dictionary
        self.op_mode_dict = {"TLE Refinement":self.tle_refinement_dict, "TLE Propagation":self.tle_prop_dict}
        #Assigning operation mode input dictionary
        self.input_op_mode_dict = {"1":"TLE Refinement", "2":"TLE Propagation"}
        #Assigning Exception handling list
        self.exception = []
        #Assigning timescale attribute
        self.ts = load.timescale()
    def Process(self):    
        #Choosing operation mode
        self.Operation_Mode()
        #Choosing file and loading 
        self.File_Selection()
        #Loading in file
        self.File_Loading()
        #Creating file content object
        self.Content_Object_Creation()
        #Operation
        self.input_file_operation()
        return
    def Operation_Mode(self):
        print("Operation Modes")
        for op_mode in self.input_op_mode_dict:
            print(op_mode, self.input_op_mode_dict[op_mode])
        #Assigning operational attributes
        self.operation_mode = self.input_op_mode_dict[input("Operation Mode:")]
        self.input_file_dict = self.op_mode_dict[self.operation_mode]
        self.input_file_directory = self.input_file_dict["Directory"]
        self.input_file_operation = self.input_file_dict["Operation"]
        self.input_file_content_class = self.input_file_dict["Content Class"]
        return
    def File_Selection(self):
        print(f"\nFiles in {self.input_file_directory} Directory")
        for file_item in os.listdir(self.input_file_directory):
            print(file_item)
        self.input_file_name = input("Input file name with extension: ")
        self.input_file_path = f"{self.input_file_directory}/{self.input_file_name}"
        return
    def File_Loading(self):
        print(f"\nLoading contents of {self.input_file_name} into program")
        #Exception Handling for loading file
        try:
            self.loaded_file = open(self.input_file_path, "r")
            self.loaded_file_contents_list = self.loaded_file.read().splitlines()
            #for line in self.loaded_file_contents_list:
                #print(line)
        except:
            self.exception.append("Error loading input file into program. Check input file directory.")
        else:
            print(f"Loaded contents of {self.input_file_name} into program")
        finally:
            self.loaded_file.close()
        return
    def Content_Object_Creation(self):
        print("\nCreating content object")
        self.TLE_object = self.input_file_content_class(self.loaded_file_contents_list).TLE_object
        print(f"Created TLE object for {self.TLE_object.sat_name} in program")
        return
    def TLE_Propagation(self):
        #Create Propagator object
        self.propagator_object = Propagator(self.TLE_object, self.ts)
        #Pass TLE object to Propagator object
        t = self.ts.utc(2024, 4, 8, 22, 45, 0)
        self.propagator_object.To_Datetime(t)
        return
    def TLE_Refinement_Process(self):
        #Refinement Loop
        #Create Propagator object
        self.propagator_object = Propagator(self.TLE_object, self.ts)
        #Pass TLE object to Propagator object
        t = self.ts.utc(2024, 4, 20, 22, 45, 0)
        self.propagator_object.To_Datetime(t)
        #Generating predicted angle list from TLE object for pass

        #Least squares regression with real pass data 

        #TLE Refinement
        return

#Defining Class TLE
class TLE():
    def __init__(self, file_contents_list):
        self.sat_name = file_contents_list[0]
        self.line1 = file_contents_list[1]
        self.line2 = file_contents_list[2]
        return

#Defining Class TLE_ANG_Content
class TLE_ANG_Content():
    def __init__(self, file_contents_list):
        self.loaded_file_contents_list = file_contents_list
        self.TLE_object = TLE(self.loaded_file_contents_list)
        self.TLE_object.sat_name = self.TLE_object.sat_name[0:5]
        return

#Defining Class TLE_Content
class TLE_Content():
    def __init__(self, file_contents_list):
        self.loaded_file_contents_list = file_contents_list
        self.TLE_object = TLE(self.loaded_file_contents_list)
        return

#Defining Class Propagator
class Propagator:
    def __init__(self, tle_object, ts):     
        #Creating skyfield Ground Station and EarthSatellite object for TLE
        self.TLE_object = tle_object
        self.ts = ts
        self.gnd_stn = wgs84.latlon(+1.29214, +103.78182, elevation_m=83)
        self.satellite = EarthSatellite(self.TLE_object.line1, self.TLE_object.line2, self.TLE_object.sat_name, self.ts)
    def To_Datetime(self, time_stamp):
        #SGP4 Propagation Algorithm with Exception Handling
        print(f'\nStarting SGP4 Propagation for {self.TLE_object.sat_name}')
        self.time_stamp = time_stamp
        #Satellite Az Al Position at time t
        self.difference_vec_func = self.satellite - self.gnd_stn
        self.topocentric_pos_vec = self.difference_vec_func.at(self.time_stamp)
        self.sat_el, self.sat_az, self.sat_distance = self.topocentric_pos_vec.altaz()
        print(f"Elevation Angle = {self.sat_el.degrees}°")
        print(f"Azimuth Angle = {self.sat_az.degrees}°")
        print(f"Distance = {self.sat_distance.km} km")
        print(f'Completed SGP4 Propagation for {self.TLE_object.sat_name}')    
        return
    def ANG_List(self):
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

#Creating instance of TLE_Refinement_Manager
Manager_Inst = TLE_Refinement_Manager()

#Run Process method for instance of TLE_Refinement_Manager
Manager_Inst.Process()