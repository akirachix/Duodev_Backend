from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from footagent.models import FootAgent

class FootAgentAPITests(APITestCase):
    def test_create_foot_agent(self):
        url = reverse('footagent-list-create')
        data = {
            "user": 1,  # Replace with actual user ID
            "agent_name": "Agent47",
            "location": "Gikomba"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_foot_agents(self):
        url = reverse('footagent-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
