from django.test import TestCase, Client


class WebTestCase(TestCase):
    def test_pages(self):
        c = Client()
        urls = [
                '/',
                '/RawData/event-flow/',
                '/RawData/event-flow-chart/',
                '/MachineLearning/ML-result/',
                '/api/RawData/event-flow/',
                '/api/RawData/data-trend/',
                '/api/rawdata/event-flow-data/?page=1&size=10',
                '/api/ml/prediction-data/?page=1&size=10'
                ]

        for url in urls:
            response = c.get(url)
            #print('Test %s \nResult:%d: %s' % (url, response.status_code, response.content))
            self.assertEqual(response.status_code, 200)
            print('Test %s Result:%d, Passed!' % (url, response.status_code))
