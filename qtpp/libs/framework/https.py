import requests


class client:
    @staticmethod
    def POST(url, data=None, json=None, **kwargs):
        response = requests.post(url, data=data, json=json, **kwargs)
        return response

    @staticmethod
    def GET(url, params=None):
        response = requests.get(url, params=params, **kwargs)
        return response