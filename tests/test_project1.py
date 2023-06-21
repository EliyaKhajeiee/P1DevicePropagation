import unittest
import project1
from pathlib import Path
import os
import contextlib
import io

class project1_test(unittest.TestCase):
    def test_check_file_crash(self):
        file_path = "wrongwrongwrong123.txt"
        with self.assertRaises(SystemExit):
            project1.check_file(file_path)

    def test_check_file_works(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
        filename = Path('testfile.txt')
        assert(project1.check_file(filename)) == True
        filename.unlink()

    def test_initial_value(self):
        file_path = os.path.join(os.getcwd(), 'testfile.txt')
        with open(file_path, 'w') as f:
            f.write("#Test case\n")
            f.write("ALERT 1 Trouble 100\n")
            f.write("CANCEL 1 Trouble 2200\n")
            f.write("ALERT 2 OhNo 1000\n")
        filename = Path("testfile.txt")
        initial_time = project1.initial_value(filename)
        self.assertEqual(initial_time, 100)
        filename.unlink()

    def test_all_things(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("LENGTH 900 \n")
            f.write("DEVICE 1\n")
            f.write("DEVICE 2\n")
            f.write("PROPAGATE 1 2 100\n")
            f.write("PROPAGATE 2 1 100\n")
            f.write("ALERT 1 Badness 200\n")
            f.write("CANCEL 1 Badness 450\n")
        filename = Path('testfile.txt')
        with io.StringIO() as output, contextlib.redirect_stdout(output):
            co = project1.check_all(filename)
            co.full_run()
            right_print ="@200: #1 SENT ALERT TO #2: Badness\n" \
                                          "@300: #2 SENT ALERT TO #1: Badness\n" \
                                          "@300: #2 RECEIVED ALERT FROM #1: Badness\n" \
                                          "@400: #1 SENT ALERT TO #2: Badness\n" \
                                          "@400: #1 RECEIVED ALERT FROM #2: Badness\n" \
                                          "@450: #1 SENT CANCELLATION TO #2: Badness\n" \
                                          "@500: #2 SENT ALERT TO #1: Badness\n" \
                                          "@500: #2 RECEIVED ALERT FROM #1: Badness\n" \
                                          "@550: #2 SENT CANCELLATION TO #1: Badness\n" \
                                          "@550: #2 RECEIVED CANCELLATION FROM #1: Badness\n" \
                                          "@600: #1 RECEIVED ALERT FROM #2: Badness\n" \
                                          "@650: #1 RECEIVED CANCELLATION FROM #2: Badness\n" \
                                          "@900: END"
            self.assertEqual(output.getvalue().strip(), right_print)
        filename.unlink()

    def test_length_less_than_alert(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("LENGTH 900 \n")
            f.write("DEVICE 1\n")
            f.write("DEVICE 2\n")
            f.write("PROPAGATE 1 2 100\n")
            f.write("ALERT 1 Badness 900\n")
        filename = Path('testfile.txt')
        with io.StringIO() as output, contextlib.redirect_stdout(output):
            co = project1.check_all(filename)
            co.full_run()
            self.assertEqual(output.getvalue().strip(), "")
        filename.unlink()

    def test_cancel_before_alert(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("LENGTH 900 \n")
            f.write("DEVICE 1\n")
            f.write("DEVICE 2\n")
            f.write("PROPAGATE 1 2 100\n")
            f.write("CANCEL 1 OhNo 500\n")
            f.write("ALERT 2 OhNo 700\n")
        filename = Path('testfile.txt')
        with io.StringIO() as output, contextlib.redirect_stdout(output):
            co = project1.check_all(filename)
            co.full_run()
            right_print = "@500: #1 SENT CANCELLATION TO #2: OhNo\n" \
                          "@600: #2 RECEIVED CANCELLATION FROM #1: OhNo\n" \
                          "@900: END"
            self.assertEqual(output.getvalue().strip(), right_print)
        filename.unlink()

    def test_cancel_only(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("LENGTH 900\n")
            f.write("DEVICE 1\n")
            f.write("DEVICE 2\n")
            f.write("PROPAGATE 1 2 100\n")
            f.write("CANCEL 1 OhNo 500\n")
        filename = Path('testfile.txt')
        with io.StringIO() as output, contextlib.redirect_stdout(output):
            co = project1.check_all(filename)
            co.full_run()
            right_print = "@500: #1 SENT CANCELLATION TO #2: OhNo\n" \
                          "@600: #2 RECEIVED CANCELLATION FROM #1: OhNo\n"\
                          "@900: END"
            self.assertEqual(output.getvalue().strip(), right_print)
        filename.unlink()

    def test_alerts_and_cancels_none_circular(self):
        with open('testfile.txt', 'w') as f:
            f.write("#Test case\n")
            f.write("LENGTH 900 \n")
            f.write("DEVICE 1\n")
            f.write("DEVICE 2\n")
            f.write("PROPAGATE 1 2 100\n")
            f.write("PROPAGATE 2 3 200\n")
            f.write("CANCEL 1 OhNo 700\n")
            f.write("ALERT 1 Ohno 100\n")
        filename = Path('testfile.txt')
        with io.StringIO() as output, contextlib.redirect_stdout(output):
            co = project1.check_all(filename)
            co.full_run()
            right_print = "@100: #1 SENT ALERT TO #2: Ohno\n"\
            "@200: #2 SENT ALERT TO #3: Ohno\n"\
            "@200: #2 RECEIVED ALERT FROM #1: Ohno\n"\
            "@400: #3 RECEIVED ALERT FROM #2: Ohno\n"\
            "@700: #1 SENT CANCELLATION TO #2: OhNo\n"\
            "@800: #2 SENT CANCELLATION TO #3: OhNo\n" \
            "@800: #2 RECEIVED CANCELLATION FROM #1: OhNo\n"\
            "@900: END"
            self.assertEqual(output.getvalue().strip(), right_print)
        filename.unlink()


if __name__ == '__main__':
    unittest.main()





