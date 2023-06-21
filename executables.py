

class Printable:
    """Class to return all my values which I give to it formatted"""
    def send_alerts(self,time,from_device,to_device,alert_desc):
        """Send alerts formatted function"""
        return f'@{time}: #{from_device} SENT ALERT TO #{to_device}: {alert_desc}'

    def send_cancellation(self,time,from_device,to_device,alert_desc):
        """Send cancellation formatted function"""
        return f'@{time}: #{from_device} SENT CANCELLATION TO #{to_device}: {alert_desc}'

    def received_alerts(self, time, from_device, to_device, alert_desc):
        """Received alerts formatted function"""
        return f'@{time}: #{to_device} RECEIVED ALERT FROM #{from_device}: {alert_desc}'

    def received_cancellation(self, time, from_device, to_device, alert_desc):
        """Received cancellation formatted function"""
        return f'@{time}: #{to_device} RECEIVED CANCELLATION FROM #{from_device}: {alert_desc}'
    def end(self,length):
        """Gives the end of the whole thing formatted function"""
        print(f'@{length}: END')