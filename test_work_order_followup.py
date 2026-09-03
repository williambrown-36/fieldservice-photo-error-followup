import unittest

from work_order_followup import needs_follow_up


class WorkOrderFollowUpTest(unittest.TestCase):
    def test_dispatched_order_without_photos_needs_technician_follow_up(self):
        self.assertTrue(needs_follow_up("dispatched", 0))
        self.assertFalse(needs_follow_up("scheduled", 0))
        self.assertFalse(needs_follow_up("dispatched", 1))
