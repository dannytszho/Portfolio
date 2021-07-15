from django.db import models

class Catagory(models.Model):
	"""A catagory for the website."""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Catagories'

	def __str__(self):
		"""Return a string representation of the model."""
		return self.text