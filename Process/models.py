from django.db import models

# Create your models here.
 
class EndPoint(models.Model):
    user_id = models.IntegerField()
    resume = models.TextField()
    job_description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return {
            'user_id':self.user_id,
            'resume':self.resume,
            'job_description':self.job_description,
            'time':self.time
        }

    