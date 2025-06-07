from django.test import TestCase
from unittest.mock import patch

from netbox_diagram.models import Diagram
from netbox_diagram.worker import UpdateDiagramCacheJob, updatecache


class UpdateDiagramCacheJobTest(TestCase):
    def setUp(self):
        self.diagram = Diagram.objects.create(name="Test Diagram")

    @patch("netbox_diagram.worker.compute_diagram_data")
    def test_run_updates_diagram_cache(self, mock_compute):
        mock_compute.return_value = {"mock": "data"}

        job = UpdateDiagramCacheJob(diagram_id=self.diagram.pk)
        job.run()

        self.diagram.refresh_from_db()
        self.assertEqual(self.diagram.cached_data, {"mock": "data"})
        mock_compute.assert_called_once_with(self.diagram.pk)

    def test_run_handles_missing_diagram(self):
        job = UpdateDiagramCacheJob(diagram_id=99999)
        try:
            job.run()
        except Exception:
            self.fail("Job raised exception on missing diagram")

    @patch("netbox_diagram.worker.UpdateDiagramCacheJob.run")
    def test_updatecache_function_calls_run(self, mock_run):
        updatecache(diagram_id=self.diagram.pk)
        mock_run.assert_called_once()
