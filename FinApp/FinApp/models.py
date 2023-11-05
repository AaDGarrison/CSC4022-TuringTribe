from django.db import models
from django.contrib.auth.models import User

class DashBoardCards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboardCardCount=models.IntegerField()

    def __str__(self):
        return self.user.username  # You can use a different field for representation