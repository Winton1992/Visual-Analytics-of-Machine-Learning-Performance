from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from ML.machine_learning import MLResult


# url 'MachineLearning/ML-result/'
class MachineLearningResultView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": 'machine-learning-result',
        }
        return render(request, "webpages/machine_learning/machine_learning_result.html", context)

    def post(self, request, *args, **kwargs):

        ml = MLResult()
        ml.run(new_data=False)

        context = {
            "title": 'machine-learning-result',
        }
        return render(request, "webpages/machine_learning/machine_learning_result.html", context)


# url 'api/MachineLearning/accuracy'
class APIMachineLearningAccuracy(APIView):

    def get(self, request, format=None, **kwargs):
        from ML.preprocessor import PreProcessor
        pp = PreProcessor()
        pp.update_data()
        mlr = MLResult()
        data = mlr.results()
        # data = {
        #     'mlp': [
        #         {"combination": "part_year", "accuracy": 0.5},
        #         {"combination": "part_year,diameter", "accuracy": 0.5},
        #         {"combination": "failure_year", "accuracy": 0.1},
        #         {"combination": "material,diameter", "accuracy": 0.4},
        #         {"combination": "length", "accuracy": 0.2},
        #         {"combination": "failure_year,diameter", "accuracy": 0.3}
        #     ],
        #     'cnn': [
        #         {"combination": "part_year", "accuracy": 0.2},
        #         {"combination": "part_year,diameter", "accuracy": 0.9},
        #         {"combination": "failure_year,diameter", "accuracy": 0.3}
        #     ],
        #     'ann': [
        #         {"combination": "part_year", "accuracy": 0.3},
        #         {"combination": "part_year,diameter", "accuracy": 0.1}
        #     ],
        #     'som': [
        #         {"combination": "part_year", "accuracy": 0.2},
        #         {"combination": "part_year,diameter", "accuracy": 0.6},
        #         {"combination": "material,diameter", "accuracy": 0.4},
        #         {"combination": "length", "accuracy": 0.2}
        #     ],
        #     'knn': [
        #         {"combination": "part_year", "accuracy": 0.2},
        #         {"combination": "part_year,diameter", "accuracy": 0.3}
        #     ],
        # }
        # print(data)
        return Response(data)


# from ML.machine_learning import MLResult  # here are the ML results
# mlr = MLResult()
# results = mlr.results()  # results of all models
#
# mdl = 'mlp'  # name of model
# attrib_list = results["best_results"][mdl]["combination"]  # input of model
# predictions = mlr.predictions(mdl, attrib_list)  # predictions based on particular model
