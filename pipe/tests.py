# from django.test import TestCase
# from .models import Pipe, Record
# from django.urls import reverse
# # Create your tests here.
#
# """
#     Model test
# """
#
#
# class PipeTestCase(TestCase):
#     def setUp(self):
#         Pipe.objects.create(part_id='UNIT_PART_ID', part_year=100, diameter=200, length=8000, material="steel")
#         pipe = Pipe.objects.get(part_id="UNIT_PART_ID")
#         Record.objects.create(pipe=pipe, failure_year=1992)
#
#     def test_pipe_can_extract(self):
#         pipe = Pipe.objects.get(part_id="UNIT_PART_ID")
#         self.assertEqual(pipe.part_year, 100)
#         self.assertEqual(pipe.diameter, 200)
#         self.assertEqual(pipe.length, 8000)
#         self.assertEqual(pipe.material, "steel")
#
#     def test_record_can_extract(self):
#         pipe = Pipe.objects.get(part_id="UNIT_PART_ID")
#         record = Record.objects.get(pipe=pipe)
#         self.assertEqual(record.failure_year, 1992)
#
# #
# # """
# #     View Test
# # """
# #
# #
# # def create_pipe(part_id, part_year, diameter, length, material):
# #     """
# #     Create a pipe
# #     """
# #     return Pipe.objects.create(part_id=part_id, part_year=part_year, diameter=diameter, length=length, material=material)
# #
# #
# # class PipeDetailViewTests(TestCase):
# #     def test_exist_item(self):
# #         """The detail view of a pipe will be displaied if item exist """
# #         pipe = create_pipe(part_id="UNIT_PART_ID_FOR_VIEW_TEST", part_year=200, diameter=300, length=9999, material="copper")
# #         url = reverse('pipe-detail', args=(pipe.pk,))
# #         response = self.client.get(url)
# #         self.assertEqual(response.status_code, 200)
# #
