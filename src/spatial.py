from src.geocode import Google_API
import json

def generate_JSON(file_path, out_path, credentials):
    try:
        with open(file_path, 'r') as zoning:
            ref = json.load(zoning)
        with open(credentials, 'r') as credential:
            api_key = json.load(credential)["key"]
        handler = Google_API(api_key)
        dic = {}
        for i in ref["zonas"].keys():
            places = ref["zonas"][i].split("/")
            lats = []
            lngs = []
            for place in places:
                lat, lng = handler.geo_request("{zona} {cidade}".format(zona=place, cidade=ref["cidade"]))
                lats.append(lat)
                lngs.append(lng)
            dic.update({i:{"name": places,"lat": sum(lats)/len(lats), "lng":sum(lngs)/len(lngs)}})
        with open(out_path, "w+") as spatial:
            spatial.write(json.dumps(dic))
        return 0
    except:
        return 1