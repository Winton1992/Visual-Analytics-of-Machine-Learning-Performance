from django.db import models


# class Pipe(models.Model):
#
#     class Meta:
#         db_table = 'pipes'
#
#     part_id = models.CharField(primary_key=True, max_length=255)
#     part_year = models.IntegerField()
#     diameter = models.IntegerField()
#     length = models.IntegerField()
#     material = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.part_id
#
#
# class Record(models.Model):
#
#     class Meta:
#         db_table = 'records'
#
#     pipe = models.ForeignKey(Pipe, on_delete=models.CASCADE)
#     failure_year = models.IntegerField()
#     failure_type = models.CharField(max_length=255)
