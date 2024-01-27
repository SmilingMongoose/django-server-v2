from django.test import TestCase
from unittest.mock import MagicMock, patch, call
from . import views
import requests
from django.urls import reverse

# unit test
class InputTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

        dummy_input = 'random input'
        response = self.client.post('', {'input_text': dummy_input})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')


# integration test that uses a mock object
class InputAndAPITestCase(TestCase):
    @patch('main_app.views.requests')
    def test_input_and_api(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Meta Data':
                {
                    '2.Symbol': 'AMZN'
                }
        }

        mock_requests.get.return_value = mock_response

        self.assertEqual(views.view_data_tmp('AMZN'), 'AMZN')
