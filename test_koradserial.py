from time import sleep
from unittest import TestCase

from koradserial import KoradSerial
from koradserial import OnOffState
from koradserial import Tracking


class KoradSerialTest(TestCase):
    def setUp(self):
        self.device = KoradSerial('/dev/tty.usbmodemfd121', True)
        self.overrideSkippedTests = False

    def tearDown(self):
        self.device.close()    

    def _pause(self, delay=1):
        """ Give the power supply time to digest the commands.

        :param delay: How long to pause. The default 1 second is overkill.
        """
        sleep(delay)

    def test_beep(self):
        """ Test the BEEP command.

        According to what I've read on the Internet, and confirmed by my trials, is that BEEP0 doesn't work.

        Thus this test is useless.

        :return:
        """
        if not self.overrideSkippedTests:
            return

        self.device.beep.off()
        status = self.device.status
        self.assertEqual(OnOffState.off, status.beep)

        self._pause()

        self.device.beep.on()
        status = self.device.status
        self.assertEqual(OnOffState.on, status.beep)

    def test_channel1(self):
        """ Test Channel 1's functionality.

        This test assumes a small load (perhaps 100 ohm) is on the power supply so a small amount of current is drawn.
        """
        channel = self.device.channels[0]

        # Turn off output and ensure that it's reading zeroes.
        self.device.output.off()
        self._pause()
        self.assertEqual(0, channel.output_voltage)
        self.assertEqual(0, channel.output_current)

        # Set the current and voltage and ensure it's reporting back correctly.
        channel.voltage = 12.34
        channel.current = 1.234
        self.assertAlmostEqual(12.34, channel.voltage, 2)
        self.assertAlmostEqual(1.234, channel.current, 3)

        # Set a different current and voltage to ensure that we're not reading old data.
        channel.voltage = 3.30
        channel.current = 0.123
        self.assertAlmostEqual(3.30, channel.voltage, 2)
        self.assertAlmostEqual(0.123, channel.current, 3)

        # Turn on the output and ensure that current is flowing across the small load.
        self.device.output.on()
        self._pause()
        self.assertAlmostEqual(3.30, channel.output_voltage, 2)
        self.assertLess(0, channel.output_current)

        self.device.output.off()

    def test_lock(self):
        """ Test the lock state.

        Ha! Just kidding. This is a stub.

        It appears that there is no command to alter the lock state.
        While connected to a serial line and processing commands, the power supply is in a lock state.
        """
        if not self.overrideSkippedTests:
            return

        pass

    def test_memory(self):
        """  Ensure that memory store/recall works.

        A two-step process is required to set a memory.
        *   First, one must choose the memory number with a `recall()` command.
        *   Second, one must set the desired voltage and current limit.
        *   Third, one must save the memory with a `save()` command.

        Recalling a memory setting simply requires calling the `recall()` command.

        This goes through the test twice with different values to ensure what is read isn't old data.
        """
        channel = self.device.channels[0]
        m1 = self.device.memories[0]
        m2 = self.device.memories[1]
        m3 = self.device.memories[2]
        m4 = self.device.memories[3]

        # Pass one with the first set  of values.

        m1.recall()
        channel.voltage = 1.00
        channel.current = 0.100
        m1.save()

        m2.recall()
        channel.voltage = 2.00
        channel.current = 0.200
        m2.save()

        m3.recall()
        channel.voltage = 3.00
        channel.current = 0.300
        m3.save()

        m4.recall()
        channel.voltage = 4.00
        channel.current = 0.400
        m4.save()

        m1.recall()
        self.assertAlmostEqual(1.00, channel.voltage, 2)
        self.assertAlmostEqual(0.100, channel.current, 3)

        m2.recall()
        self.assertAlmostEqual(2.00, channel.voltage, 2)
        self.assertAlmostEqual(0.200, channel.current, 3)

        m3.recall()
        self.assertAlmostEqual(3.00, channel.voltage, 2)
        self.assertAlmostEqual(0.300, channel.current, 3)

        m4.recall()
        self.assertAlmostEqual(4.00, channel.voltage, 2)
        self.assertAlmostEqual(0.400, channel.current, 3)

        # Pass two with different values.

        m1.recall()
        channel.voltage = 5.00
        channel.current = 0.500
        m1.save()

        m2.recall()
        channel.voltage = 10.00
        channel.current = 1.000
        m2.save()

        m3.recall()
        channel.voltage = 15.00
        channel.current = 1.500
        m3.save()

        m4.recall()
        channel.voltage = 20.00
        channel.current = 2.000
        m4.save()

        m1.recall()
        self.assertAlmostEqual(5.00, channel.voltage, 2)
        self.assertAlmostEqual(0.500, channel.current, 3)

        m2.recall()
        self.assertAlmostEqual(10.00, channel.voltage, 2)
        self.assertAlmostEqual(1.000, channel.current, 3)

        m3.recall()
        self.assertAlmostEqual(15.00, channel.voltage, 2)
        self.assertAlmostEqual(1.500, channel.current, 3)

        m4.recall()
        self.assertAlmostEqual(20.00, channel.voltage, 2)
        self.assertAlmostEqual(2.000, channel.current, 3)

    def test_model(self):
        """ Test the IDN command.

        Read the model number from the device.
        """
        model = self.device.model
        self.assertTrue(model.startswith("KORAD"))

    def test_ocp(self):
        """ Test Over Current Protection

        There's no way to get feedback on these, so simply ensure that no exceptions are thrown.
        """
        self.device.over_current_protection.on()
        self._pause()
        self.device.over_current_protection.off()

    def test_ovp(self):
        """ Test Over Voltage Protection

        There's no way to get feedback on these, so simply ensure that no exceptions are thrown.
        """
        self.device.over_voltage_protection.on()
        self._pause()
        self.device.over_voltage_protection.off()

    def test_output(self):
        """ Ensure the device is reporting the output on/off state correctly.
        """
        self.device.output.on()
        status = self.device.status
        self.assertEqual(OnOffState.on, status.output)

        self._pause()

        self.device.output.off()
        status = self.device.status
        self.assertEqual(OnOffState.off, status.output)

    def test_track(self):
        """ Test the TRACK commands.

        **NOTE:** The tests here are hypothetical.
        I don't have a multi-channel power supply to actually test this against.
        """
        if not self.overrideSkippedTests:
            return

        self.device.track(Tracking.parallel)
        status = self.device.status
        self.assertEqual(Tracking.parallel, status.tracking)

        self._pause()

        self.device.track(Tracking.series)
        status = self.device.status
        self.assertEqual(Tracking.series, status.tracking)

        self._pause()

        self.device.track(Tracking.independent)
        status = self.device.status
        self.assertEqual(Tracking.independent, status.tracking)
