from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
    # this is a tuple with multiple tuples
    # each of these is called a 2-tuple
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

# Create your models here.
class Finch(models.Model):
  name = models.CharField(max_length=100)
  breed = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()

  def __str__(self):
    return self.name
  
  # get_aboslute_url method
  def get_absolute_url(self):
    return reverse('detail', kwargs={'finch_id': self.id})
  
  def fed_for_today(self):
    return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )

    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date} for {self.finch}"
    
    # change the default sort
    class Meta:
        ordering = ['-date']