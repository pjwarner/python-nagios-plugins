#!/usr/bin/python

import unittest
import check_bandwidth

class testing(unittest.TestCase):
    def setup(self):
        self.alert_values = [200000, 225001, 237501]

    def test_month_alert_output(self):
        month_alert_values = [200000, 225001, 237501]
        self.assertEqual(check_bandwidth.monthly_status(month_alert_values[0],0.95,0.90)[:2],'OK')
        self.assertEqual(check_bandwidth.monthly_status(month_alert_values[1],0.95,0.90)[:7],'WARNING')
        self.assertEqual(check_bandwidth.monthly_status(month_alert_values[2],0.95,0.90)[:8],'CRITICAL')

    def test_day_alert_output(self):
        day_alert_values = [7000, 7501, 7917]
        self.assertEqual(check_bandwidth.daily_status(day_alert_values[0],0.95,0.90)[:2],'OK')
        self.assertEqual(check_bandwidth.daily_status(day_alert_values[1],0.95,0.90)[:7],'WARNING')
        self.assertEqual(check_bandwidth.daily_status(day_alert_values[2],0.95,0.90)[:8],'CRITICAL')

if __name__ == '__main__':
    unittest.main()
            
    
        
