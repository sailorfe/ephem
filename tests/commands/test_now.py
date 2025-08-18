import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
from ephem.commands import now

class TestNow(unittest.TestCase):
    def test_get_moment_utc(self):
        """Test that get_moment returns current time in UTC when no timezone given"""
        dt_local, dt_utc, approx = now.get_moment()
        
        # Check timezone info
        self.assertEqual(dt_local.tzinfo, ZoneInfo("UTC"))
        self.assertEqual(dt_utc.tzinfo, ZoneInfo("UTC"))
        
        # Local and UTC should be equal when both are UTC
        self.assertEqual(dt_local, dt_utc)
        
        # Time should be current (within a few seconds)
        current = datetime.now(ZoneInfo("UTC"))
        time_diff = abs((current - dt_utc).total_seconds())
        self.assertLess(time_diff, 5)  # Within 5 seconds
        
        # Should never be approximate time
        self.assertFalse(approx)

    def test_get_moment_timezone(self):
        """Test that get_moment handles timezone conversion"""
        dt_local, dt_utc, approx = now.get_moment("America/New_York")
        
        # Check timezone info
        self.assertEqual(dt_local.tzinfo, ZoneInfo("America/New_York"))
        self.assertEqual(dt_utc.tzinfo, ZoneInfo("UTC"))
        
        # Local time should be behind UTC
        self.assertLess(dt_local.hour, dt_utc.hour)
        
        # Should never be approximate time
        self.assertFalse(approx)

if __name__ == '__main__':
    unittest.main()