import sys
from pathlib import Path

import executables
import file_organizer
import os
#C:\Users\Eliya\PycharmProjects\Project1\samples\sample_input.txt
#C:\Users\Eliya\PycharmProjects\Project1\samples\sample_input_sanity.txt
def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input, don't know to unittest input statements as
    stated in EDdiscussion we don't need to hit this block."""
    return Path(input())

def check_file(file_path):
    """Checks if a file exists and if not prints an output and exits the code"""
    if os.path.isfile(file_path):
        return True
    else:
        print("FILE NOT FOUND")
        sys.exit(1)

def initial_value(input_file_path):
    """Gets back the initial value of where the alerts or cancels start"""
    check_file(input_file_path)
    fo = file_organizer.File_Organizer(input_file_path)
    alert_dict, cancel_dict = fo.get_alerts()
    try:
        initial_time = int(list(alert_dict.values())[0]["time"])
    except IndexError:
        initial_time = int(list(cancel_dict.values())[0]["time"])

    for key_values in alert_dict:
        new_time = alert_dict[key_values]["time"]
        if int(new_time) < initial_time:
            initial_time = int(new_time)
    for key_values in cancel_dict:
        new_time = cancel_dict[key_values]["time"]
        if int(new_time) < initial_time:
            initial_time = int(new_time)
    return initial_time

class check_all:
    """My full class for running the majority of the alert propagating"""
    def __init__(self,file_location):
        """Initially putting values for all the different things I need to call in my class."""
        self.device_list = {} #use this
        self.alert_dict = {}
        self.cancel_dict = {}
        self.file_location = file_location
        self.current_time = 0
        self.total_list = []
        self.alert_times = []
        self.cancel_times = []
        self.total_times = []
        self.last_device_from = 0
        self.last_device_to = 0
        self.alert_desc = ""
        self.cancel_desc = ""
        self.real_list = []
    def propagate_alerts(self): #TO SEND MY ALERT: WORKS FOR MORE THAN 1 ALERT
        """Propagates the starting alerts and adds them to the list"""
        check_file(self.file_location)
        fo = file_organizer.File_Organizer(self.file_location)
        alert_dict, cancel_dict = fo.get_alerts()
        prop_dict = fo.get_propagate()
        p = executables.Printable()
        for from_device, to_device in prop_dict.keys():
            self.device_list.setdefault(from_device, {})
            self.device_list[from_device][to_device] = prop_dict[(from_device, to_device)]
        for alert_desc, alert_info in alert_dict.items(): #each alert
                for (from_device, to_device), prop_delay in prop_dict.items(): #each propagation
                    if int(alert_info['ID']) == int(from_device): #whenever the from device = the ID
                        to_add = p.send_alerts(int(alert_info['time']), from_device, to_device, alert_desc)
                        if self.cancel_dict.get(from_device, []) and (self.cancel_dict[from_device][0]['desc'] == alert_desc and self.current_time >=
                                self.cancel_dict[from_device][0]['time']):
                            pass
                        else:
                            self.total_list.append(to_add)
                            self.real_list.append(to_add)
    def propagate_cancels(self): #TO SEND MY CANCELLATIONS, WORKS FOR MORE THAN 1 CANCELLATIONS
        """Propagates the cancels from the starts and adds them to a list"""
        check_file(self.file_location)
        fo = file_organizer.File_Organizer(self.file_location)
        alert_dict, cancel_dict = fo.get_alerts()
        prop_dict = fo.get_propagate()
        p = executables.Printable()
        for cancel_desc, cancel_info in cancel_dict.items():
                for (from_device, to_device), prop_delay in prop_dict.items():
                    if int(cancel_info['ID']) == int(from_device):
                        to_add = p.send_cancellation(int(cancel_info['time']), from_device, to_device, cancel_desc)
                        self.total_list.append(to_add)
                        self.real_list.append(to_add)
                        var = int(cancel_info['time'])
                        self.cancel_dict[from_device] = [{'desc': cancel_desc, 'time': var}]

    def propagate_alerts_device(self): #GIVES TIMES CORRECT AND BREAKS OUT OF THESE, NEED TO FIX THE ALERTS AND CANCELLATIONS PRINTING AT WRONG TIMES
        """Works for all alerts and cancels that are in order, if the propagated is out of order the code will print the wrong output, adds all my alerts and cancels to a list """
        check_file(self.file_location)
        fo = file_organizer.File_Organizer(self.file_location)
        alert_dict, cancel_dict = fo.get_alerts()
        prop_dict = fo.get_propagate()
        p = executables.Printable()
        length = fo.get_length()
        for each_time, (cancel_desc, cancel_info) in zip(self.cancel_times, cancel_dict.items()):
            count_cancels = 0
            checker = cancel_info['ID'] #Gives the ID for the Cancel IDs
            t = True
            self.current_time = each_time #gives each time and should iterate through them #starting TIME for each one
            while t:
                for (from_device, to_device), prop_delay in prop_dict.items(): #gives correctly each to_device and from_device and the delay
                    if self.current_time < length: #makes sure the cancel times are not over the length
                        if self.current_time >= int(cancel_info['time']):
                            if int(from_device) == int(checker):
                                adding = p.send_cancellation(self.current_time, from_device,
                                                             to_device,
                                                             cancel_desc)
                                adding_rec = p.received_cancellation(self.current_time + prop_delay,
                                                                     from_device,
                                                                     to_device, cancel_desc)
                                self.real_list.append(adding)
                                self.real_list.append(adding_rec)
                                self.current_time += prop_delay
                                count_cancels += 1
                                checker = to_device
                                if to_device in self.cancel_dict:
                                    self.cancel_dict[to_device].append(
                                        {'desc': cancel_desc, 'time': self.current_time})
                                else:
                                    self.cancel_dict[to_device] = [
                                        {'desc': cancel_desc, 'time': self.current_time}]
                            if count_cancels == len(prop_dict.items()):
                                t = False
        for each_time, (alert_desc, alert_info) in zip(self.alert_times, alert_dict.items()):
            count = 0
            # do something with each_time, alert_desc, and alert_info
            self.current_time = each_time
            self.total_list = []
            checker = alert_info["ID"]
            while self.current_time < length:
                    for (from_device, to_device), prop_delay in prop_dict.items():
                            if self.cancel_dict.get(from_device, []) and (self.cancel_dict[from_device][0]['desc'] == alert_desc and self.current_time >=
                                    self.cancel_dict[from_device][0]['time']): #check if for THAT EXACT TIME, THE Cancel hasn't been sent yet if so it moves on, if not iterate
                                self.current_time += prop_delay
                            else:
                                if self.current_time >= int(alert_info['time']):
                                    if int(from_device) == int(checker):
                                        self.alert_desc = alert_desc
                                        adding = p.send_alerts(self.current_time, from_device,
                                                               to_device, alert_desc)
                                        adding_rec = p.received_alerts(self.current_time + prop_delay,
                                                                       from_device, to_device,
                                                                       alert_desc)
                                        self.total_list.append(adding)
                                        self.total_list.append(adding_rec)
                                        self.real_list.append(adding)
                                        self.real_list.append(adding_rec)
                                        checker = to_device
                                        self.current_time += prop_delay
                                    else:
                                        count += 1
                                if count > len(prop_dict.items())*len(prop_dict.items()):
                                    self.current_time = length

    def the_end(self):
        """Prints all my ending statements while also iterating through my list and printing the correct values out """
        fo = file_organizer.File_Organizer(self.file_location)
        length = fo.get_length()
        p = executables.Printable()
        final_set = set(self.real_list)
        final_set = list(final_set)
        final_set.sort(key = lambda x: (
            int(x.split(":")[0][1:]),"SEND" not in x,"RECEIVED" in x))
        #lots of testing to get this to sort properly
        for alert in final_set:
            if int(alert.split(":")[0][1:]) < length:
                print(alert)

        p.end(length)

    def full_run(self):
        """Runs the entire code in my class calling the self functions"""
        check_file(self.file_location)
        fo = file_organizer.File_Organizer(self.file_location)
        alert_dict, cancel_dict = fo.get_alerts()
        length = fo.get_length()
        initial_time = initial_value(self.file_location)
        self.current_time = initial_time #this is going to give us starting TIME

        for alert_desc, alert_info in alert_dict.items():
            self.alert_times.append(int(alert_info['time']))
        for cancel_desc, cancel_info in cancel_dict.items():
            self.cancel_times.append(int(cancel_info['time']))
        self.total_times = sorted(self.alert_times + self.cancel_times)
        #This is going to give us a sorted list with all the times of alerts or cancellations

        while (alert_dict or cancel_dict) and self.current_time < length:
            min_time = int(length)
            if alert_dict:
                for times in alert_dict:
                    if int(alert_dict[times]['time']) < min_time:
                        min_time = int(alert_dict[times]['time'])
            if cancel_dict:
                for times in cancel_dict:
                    if int(cancel_dict[times]['time']) < min_time:
                        min_time = int(
                            cancel_dict[times]['time']) # THE STARTING TIME OF PROPAGATION
            self.propagate_cancels() #this works almost
            self.propagate_alerts() #this works almost
            self.propagate_alerts_device()
            if self.alert_dict == {}:
                self.current_time = length
            self.the_end()


def main() -> None:
    """Runs the simulation program in its entirety, can't unittest main function"""
    input_file_path = _read_input_file_path()
    run = check_all(input_file_path)
    run.full_run()

if __name__ == '__main__':
    main()