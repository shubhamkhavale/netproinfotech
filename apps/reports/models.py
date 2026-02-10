from django.db import models

class ReportLog(models.Model):
    report_name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_name
