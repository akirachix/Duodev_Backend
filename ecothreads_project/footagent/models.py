from django.db import models
from django.conf import settings
from textilebale.models import TextileBale  # Import TextileBale model for assignments

class FootAgent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.agent_name

class AgentAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    foot_agent = models.ForeignKey(FootAgent, on_delete=models.CASCADE, related_name='assignments')
    textile_bale = models.ForeignKey(TextileBale, on_delete=models.CASCADE, related_name='assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.foot_agent.agent_name} assigned to {self.textile_bale.bale_id}'
