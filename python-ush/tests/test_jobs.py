import unittest
import subprocess
import time
from ush.jobs import JobManager, Job

class TestJobManager(unittest.TestCase):

    def setUp(self):
        self.job_manager = JobManager()

    def test_add_job(self):
        # Create a simple process
        process = subprocess.Popen(['ping', 'localhost', '-n', '2'] if subprocess.os.name == 'nt' else ['sleep', '0.1'])
        job_id = self.job_manager.add_job('test command', process)
        self.assertIn(job_id, self.job_manager.jobs)
        self.assertEqual(self.job_manager.jobs[job_id].command, 'test command')
        process.wait()  # Clean up

    def test_remove_job(self):
        process = subprocess.Popen(['ping', 'localhost', '-n', '1'] if subprocess.os.name == 'nt' else ['sleep', '0.1'])
        job_id = self.job_manager.add_job('test command', process)
        self.assertIn(job_id, self.job_manager.jobs)
        self.job_manager.remove_job(job_id)
        self.assertNotIn(job_id, self.job_manager.jobs)
        process.wait()  # Clean up

    def test_get_jobs(self):
        process1 = subprocess.Popen(['ping', 'localhost', '-n', '3'] if subprocess.os.name == 'nt' else ['sleep', '0.5'])
        process2 = subprocess.Popen(['ping', 'localhost', '-n', '3'] if subprocess.os.name == 'nt' else ['sleep', '0.5'])
        job_id1 = self.job_manager.add_job('command1', process1)
        job_id2 = self.job_manager.add_job('command2', process2)
        
        jobs = self.job_manager.get_jobs()
        self.assertIn(job_id1, jobs)
        self.assertIn(job_id2, jobs)
        
        # Clean up
        process1.wait()
        process2.wait()

    def test_job_completion(self):
        process = subprocess.Popen(['ping', 'localhost', '-n', '1'] if subprocess.os.name == 'nt' else ['sleep', '0.1'])
        job_id = self.job_manager.add_job('test command', process)
        job = self.job_manager.jobs[job_id]
        
        # Initially not completed
        self.assertFalse(job.is_completed())
        
        # Wait for completion
        process.wait()
        time.sleep(0.1)  # Small delay to ensure completion is detected
        
        # Should be completed now
        self.assertTrue(job.is_completed())

    def test_update_jobs(self):
        process = subprocess.Popen(['ping', 'localhost', '-n', '1'] if subprocess.os.name == 'nt' else ['sleep', '0.1'])
        job_id = self.job_manager.add_job('test command', process)
        job = self.job_manager.jobs[job_id]
        
        # Initially running
        self.assertEqual(job.status, 'running')
        
        # Wait and update
        process.wait()
        self.job_manager.update_jobs()
        
        # Should be completed now
        self.assertEqual(job.status, 'completed')
    
    def test_job_id_increment(self):
        process1 = subprocess.Popen(['ping', 'localhost', '-n', '1'] if subprocess.os.name == 'nt' else ['sleep', '0.1'])
        process2 = subprocess.Popen(['ping', 'localhost', '-n', '1'] if subprocess.os.name == 'nt' else ['sleep', '0.1'])
        
        job_id1 = self.job_manager.add_job('command1', process1)
        job_id2 = self.job_manager.add_job('command2', process2)
        
        self.assertEqual(job_id2, job_id1 + 1)
        
        # Clean up
        process1.wait()
        process2.wait()

if __name__ == '__main__':
    unittest.main()