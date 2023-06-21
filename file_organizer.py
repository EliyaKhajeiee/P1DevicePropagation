

class File_Organizer:
    """Class to get all my variables from the file"""
    def __init__(self,filename):
        """Initialize all my instance variables"""
        self.filename = filename
        self.propagation = {}
        self.alerts_alert = {}
        self.alerts_cancel = {}
        self.devices_with_id= []

    def get_length(self):
        """Gets the length that is given inside a file"""
        with open(self.filename, "r") as content:
            for single_line in content:
                if single_line.startswith("LENGTH"):
                    full_Length = single_line.split()[1]
                    return int(full_Length)

    def get_propagate(self):
        """Gets the propagation of the devices into a dict"""
        with open(self.filename, "r") as content:
            for single_line in content:
                if single_line.startswith("PROPAGATE"):
                    split_lines = single_line.strip().split(" ")
                    from_device = int(split_lines[1])
                    to_device = int(split_lines[2])
                    delay_time = int(split_lines[3])
                    self.propagation[(from_device, to_device)] = delay_time
        return self.propagation

    def get_alerts(self):
        """Gets the alerts and their time added to a dictionary"""
        with open(self.filename, "r") as content:
            for single_line in content:
                if single_line.startswith("ALERT"):
                    split_lines = single_line.strip().split(" ")
                    alert = split_lines[0]
                    device_ID = split_lines[1]
                    alert_description = split_lines[2]
                    sim_time = split_lines[3]
                    self.alerts_alert[alert_description] = {"alert": alert, "time": sim_time,
                                                          "ID": device_ID}
                if single_line.startswith("CANCEL"):
                    split_lines = single_line.strip().split(" ")
                    alert = split_lines[0]
                    device_ID = split_lines[1]
                    alert_description = split_lines[2]
                    sim_time = split_lines[3]
                    self.alerts_cancel[alert_description] = {"alert": alert, "time": sim_time,
                                                          "ID": device_ID}
        return self.alerts_alert,self.alerts_cancel
    def get_devices_list(self):
        """Gets a list of devices from the file"""
        with open(self.filename, "r") as content:
            for single_line in content:
                if single_line.startswith("DEVICE"):
                    split_lines = single_line.strip().split(" ")
                    DEVICES_WITH_ID = split_lines[1]
                    self.devices_with_id.append(DEVICES_WITH_ID)
        return self.devices_with_id







