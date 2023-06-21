import unittest
import io
import contextlib
import executables
class Executables_test(unittest.TestCase):
        def test_send_alerts(self):
            prnt = executables.Printable()
            a = prnt.send_alerts(0, 1, 2, "Trouble")
            self.assertEqual(a, "@0: #1 SENT ALERT TO #2: Trouble")

        def test_send_cancellation(self):
            prnt = executables.Printable()
            a = prnt.send_cancellation(0, 1, 2, "Trouble")
            self.assertEqual(a, "@0: #1 SENT CANCELLATION TO #2: Trouble")

        def test_received_alerts(self):
            prnt = executables.Printable()
            a = prnt.received_alerts(0, 1, 2, "Trouble")
            self.assertEqual(a, "@0: #2 RECEIVED ALERT FROM #1: Trouble")

        def test_received_cancellation(self):
            prnt = executables.Printable()
            a = prnt.received_cancellation(0, 1, 2, "Trouble")
            self.assertEqual(a, "@0: #2 RECEIVED CANCELLATION FROM #1: Trouble")

        def test_end(self):
            prnt = executables.Printable()
            with contextlib.redirect_stdout(io.StringIO()) as output:
                prnt.end("9999")
            self.assertEqual(output.getvalue().strip(), "@9999: END")

if __name__ == '__main__':
    unittest.main()
