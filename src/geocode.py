import requests
import json

class Google_API:
    def __init__(self, key):
        self.URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
        self.key = key

    def geo_request(self, place):
        request_URL = "{url}{address}&key={key}".format(url = self.URL, address=self.generate(place), key=self.key)
        response = json.loads(requests.get(request_URL).text)
        return response["results"][0]["geometry"]["location"]["lat"], response["results"][0]["geometry"]["location"]["lng"]

    def generate(self, string):
        string = string.strip().split(' ')
        plus = "+"
        aux = ""
        for index in range(len(string)):
            aux = aux + string[index] + plus
        return aux