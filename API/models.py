from django.db import models

# Create your models here.
 
class EndPoint(models.Model):
    user_name = models.TextField()
    user_id = models.IntegerField()
    resume = models.TextField()
    prompt = models.TextField()
    job_description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return {"username":self.user_name,'user_id':self.user_id,'resume':self.resume,'prompt':self.prompt,'job_description':self.job_description,'time':self.time}

    