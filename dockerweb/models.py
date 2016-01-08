from django.db import models

# Create your models here.
#####docker
class cmdb_docker_port(models.Model):
        docker_ip=models.CharField(max_length=500)
        docker_port=models.CharField(max_length=500)
        docker_name=models.CharField(max_length=500)
        class Meta:
                db_table = 'docker_port'
        def __unicode__(self):
                return self.docker_ip

    