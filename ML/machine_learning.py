import ML.basic_neural_net_classifier as mlp
from operator import itemgetter
import json
from ML.preprocessor import PreProcessor
import ML.svm_model as svm

class MLResult:

    def __init__(self):
        pass

    def run(self, new_data=False):
        """
        Call this method each time a new csv is uploaded
        """
        print(
            """\n
            The two files uploaded should be pdata.csv and pfail.csv
            and should be located in static/csv/upload.

            The merged file output will be data.csv
            and will be located in static/csv

            Running the algorithms over large datasets takes time!
            For testing, try the files in the aptly named:
            static/csv/not_unreasonably_large_dataset
            \b"""
        )
        if new_data:
            pp = PreProcessor()
            pp.update_data()
        return self.results(run_algorithms=True)

    def results(self, run_algorithms=False):

        if run_algorithms:
            results = {
                'mlp': mlp.results(), #json.loads('[{"combination": "FY", "accuracy": 48}]'),
                'svm': svm.results()
            }
            """Add a mapping of the best performance in each algorithm"""
            best_results = [

                {alg: sorted(results[alg], key=itemgetter("accuracy")).pop()}
                            for alg in results.keys()

                ]

            results["best_results"] = best_results
            with open("ML/saved_results.json",'w') as saved:
                saved.write(json.dumps(results))
        else:
            try:
                with open("ML/saved_results.json", 'r') as results:
                    return json.load(results)
            except Exception:
                print("open failed")
                return self.results(run_algorithms=True)
        return results

    def predictions(self, mdl, attrib_list, prediction_range=1, failure_year=2014):
        if mdl == 'mlp':
            return mlp.predictions(attrib_list,
                                  prediction_range=prediction_range,
                                   failure_year=failure_year)
        if mdl == 'svm':
            return None
