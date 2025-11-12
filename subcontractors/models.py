from django.db import models

from projects.models import Project


class Subcontractor(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class SubcontractorAssignment(models.Model):
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name='subcontractor_assignments')
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
    work_description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.subcontractor.name} - {self.project.title}"
