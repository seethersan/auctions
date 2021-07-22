from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class UserDetails(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	balance = models.DecimalField(max_digits=6, decimal_places=2)
	cellphone = models.CharField(max_length=10)
	address = models.CharField(max_length=255)
	town = models.CharField(max_length=45)
	postal_code = models.CharField(max_length=45)
	country = models.CharField(max_length=45)
	max_bid = models.FloatField(validators=[MinValueValidator(0.0)])

	def __str__(self):
		user = User.objects.get(id=self.user)
		return "id=" + str(self.pk) + " username=" + user.username + " email=" + user.email
