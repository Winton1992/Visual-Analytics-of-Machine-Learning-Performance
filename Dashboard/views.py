from django.shortcuts import render
from django.views.generic import View
from ML.machine_learning import MLResult


# url '/'
class DashboardView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "title": 'dashboard',
        }
        return render(request, "webpages/dashboard.html", context)

    def post(self, request, *args, **kwargs):

        # ml = MLResult()
        # ml.run()
        from ML.preprocessor import PreProcessor
        pp = PreProcessor()
        pp.update_data()

        context = {
            "title": 'dashboard',
        }
        return render(request, "webpages/dashboard.html", context)