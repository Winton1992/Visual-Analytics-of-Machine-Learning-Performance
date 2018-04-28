from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import csv
from csv2json import convert, load_csv, save_json



# url 'RawData/event-flow/'
class RawDataEventFlowView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": 'raw-data-event-flow',
        }
        return render(request, "webpages/raw_data_event_flow.html", context)


# url 'RawData/event-flow/'
class RawDataEventFlowChartView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": 'raw_data_event_flow_chart',
        }
        return render(request, "webpages/raw_data_event_flow_chart.html", context)


# url 'RawData/data-trend/'
class RawDataDataTrendView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": 'raw-data-data-trend',
        }
        return render(request, "webpages/raw_data_data_trend.html", context)


# url api/RawData/data-trend/
class APIRawDataDataTrendView(APIView):
    def get(self, request, format=None, **kwargs):
        # with open('static/json/data.json', newline='') as jsonfile:
        #     data = json.load(jsonfile)
        # return Response(data)
        # with open('static/csv/data.csv', newline='') as csvfile:
        #    data = csv.DictReader(csvfile)
        #    return Response(data)
        with open('static/csv/data.csv') as r, open('static/json/data.json', 'w') as w:
            convert(r, w)

        with open('static/json/data.json', newline='') as jsonfile:
            data = json.load(jsonfile)
            return Response(data)


# url api/RawData/event-flow/
class APIRawDataEventFlowView(APIView):
    def get(self, request, format=None, **kwargs):

        rows = [{
            'ENTITY_ID': 'e1',
            'TS': '60000',
            'EVENT_NAME': 'Alex'
        }]
        i = 0
        event_id = ''
        min_year = 1990
        with open('static/csv/events.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile)
            for row in spamreader:
                if (i > 0):
                    begin_year = int(row["part_year"])
                    if (event_id != row["part_id"]):
                        event_id = row["part_id"]
                        item = {
                            "ENTITY_ID": "E" + row["part_id"],
                            "TS": begin_year * 1000.0,
                            "EVENT_NAME": row["material"]
                        }
                        rows.append(item)
                    item = {
                        "ENTITY_ID": "E" + row["part_id"],
                        "TS": (int(row["failure_year"])) * 1000.0,  # + begin_year* 365 * 24 * 3600
                        "EVENT_NAME": row["material"]
                    }
                    rows.append(item)
                i = i + 1

        # print("rows: %s" % rows)

        data = {
            'ourEvents': {
                'userEvents': {
                    'usr1': [{
                        'ENTITY_ID': 'e1',
                        'TS': '300',
                        'EVENT_NAME': 'steel'
                    }],
                    'usr2': [{
                        'ENTITY_ID': 'e2',
                        'TS': '420',
                        'EVENT_NAME': 'copper'
                    }]
                },
                'allEvents': rows
            }
        }
        return Response(data)


# django_angular_demo
class django_angular_demo(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "title": 'django angular demo',
        }

        return render(request, "webpages/django_angular_demo.html", context)


class combine_pipe_files(APIView):
    def get(self, request, format=None, **kwargs):
        rows_pipe = []
        with open('Data/pdata.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            title = reader.fieldnames
            for row in reader:
                rows_pipe.extend([{title[i]: row[title[i]] for i in range(len(title))}])

        rows_fails = []
        with open('Data/pfail.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            title = reader.fieldnames
            for row in reader:
                rows_fails.extend([{title[i]: row[title[i]] for i in range(len(title))}])

        # Part ID,Install Year,Diameter Size,Length,Material
        # Part ID,Failure_Year
        rows = []
        for row in rows_pipe:
            ev = {
                "part_id": row["Part ID"],
                "part_year": row["Install Year"],
                "diameter": row["Diameter Size"],
                "length": row["Length"],
                "material": row["Material"],
                "failure_year": ""
            }

            filter_rows = list(filter(lambda x: x["Part ID"] == row["Part ID"], rows_fails))
            for fr in filter_rows:
                ev = {
                    "part_id": row["Part ID"],
                    "part_year": row["Install Year"],
                    "diameter": row["Diameter Size"],
                    "length": row["Length"],
                    "material": row["Material"],
                    "failure_year": fr["Failure_Year"]
                }
                rows.append(ev)

        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        return Response(rows)


class APIRawDataEventFlowData(APIView):
    def get(self, request, format=None, **kwargs):
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        page = (1, int(page))[page is not None and page.isnumeric()]
        size = (100, int(size))[size is not None and size.isnumeric()]
        #print("page: %s, size: %s" % (page, size))
        #part_id,failure_year,part_year,diameter,length,material,has_failed
        rows = []
        skip = (page - 1) * size
        index = 0
        total_partid_list = set()
        current_partid_list = set()
        with open('static/csv/data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            title = reader.fieldnames
            for row in reader:
                index += 1
                total_partid_list.add(row["part_id"])
                if len(total_partid_list) > skip and len(current_partid_list) < size:
                    rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
                    current_partid_list.add(row["part_id"])
                    # if len(current_partid_list) >= size:
                    #     break

        r = {
            "total": len(total_partid_list),
            "items": rows,
            "raw_records": index
        }

        return Response(r)


# url api/rawdata/event-flow-data
class APIRawDataEventFlowData_old(APIView):
    def get(self, request, format=None, **kwargs):
        rows = []
        with open('static/csv/events.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            title = reader.fieldnames
            for row in reader:
                rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
                # jsontext = json.dumps(rows, sort_keys=False, indent=4, separators=(',', ': '), encoding="utf-8",
                #            ensure_ascii=False)

                # print("rows: %s" % rows)

        return Response(rows)


