from unittest.mock import patch
from django.test import TestCase


class APITestBase(TestCase):

    def setUp(self):
        self.auth_mock = self.create_patch('rest_framework.views.APIView.check_permissions')
        self.auth_mock.return_value = True

        super().setUp()

    def create_patch(self, path, **kwargs):
        patcher = patch(path, **kwargs)
        return self.start_patch(patcher)

    def start_patch(self, patcher):
        mock_instance = patcher.start()
        self.addCleanup(patcher.stop)
        return mock_instance
