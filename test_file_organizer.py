import unittest
import file_organizer
from pathlib import Path


class file_organizer_test(unittest.TestCase):
    def test_file_length_works(self):
        #filename = _read_input_file_path() #see if this is how to do it
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("LENGTH 9999")
        filename = Path('testfile.txt')
        fo = file_organizer.File_Organizer(filename)
        length = fo.get_length()
        self.assertEqual(length, 9999)
        filename.unlink()

    def test_get_propagate(self):
        #filename = _read_input_file_path()
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("PROPAGATE 1 2 750\n")
            f.write("PROPAGATE 2 3 1250\n")
            f.write("PROPAGATE 3 4 500\n")
            f.write("PROPAGATE 4 1 1000\n")
        filename = Path('testfile.txt')
        fo = file_organizer.File_Organizer(filename)
        right_dict = fo.get_propagate()
        right_dict_test =  {(1, 2): 750, (2, 3): 1250, (3, 4): 500, (4, 1): 1000}
        self.assertEqual(right_dict, right_dict_test)
        filename.unlink()

    def test_get_alerts_alert_and_cancel(self):
        #filename = _read_input_file_path()
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("ALERT 1 Trouble 0\n")
            f.write("CANCEL 1 Trouble 2200\n")
        filename = Path('testfile.txt')
        fo = file_organizer.File_Organizer(filename)
        alert_dict,cancel_dict = fo.get_alerts()
        right_cancel_dict = {'Trouble': {'alert': 'CANCEL', 'time': '2200', 'ID': '1'}}
        right_alert_dict = {'Trouble': {'alert': 'ALERT', 'time': '0', 'ID': '1'}}
        self.assertEqual(alert_dict,right_alert_dict)
        self.assertEqual(cancel_dict,right_cancel_dict)
        filename.unlink()

    def test_get_devices(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("DEVICE 1\n")
            f.write("DEVICE 2\n")
            f.write("DEVICE 3\n")
        filename = Path('testfile.txt')
        fo = file_organizer.File_Organizer(filename)
        devices_with_id = fo.get_devices_list()
        right_list = ["1","2","3"]
        self.assertEqual(right_list,devices_with_id)
        filename.unlink()

if __name__ == '__main__':
    unittest.main()

