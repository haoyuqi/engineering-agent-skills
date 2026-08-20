import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from retry_worker import enqueue_retry


class RetryWorkerTest(unittest.TestCase):
    def test_retry_is_idempotent_for_same_job(self):
        queue = []
        accepted_job_ids = set()
        self.assertTrue(enqueue_retry("job-1", queue, accepted_job_ids))
        self.assertFalse(enqueue_retry("job-1", queue, accepted_job_ids))
        self.assertEqual(queue, ["job-1"])


if __name__ == "__main__":
    unittest.main()
