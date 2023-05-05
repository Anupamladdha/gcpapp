import requests
import json
import pprint as pp


def pathlen(lat1, long1, lat2, long2):
    apikey = "AIzaSyAGAjAGWOVhufu1j3YkkN8iVo0vmhzLMtI"
    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
    origin = f"{lat1}, {long1}"
    url2 = "&destinations="
    destination = f"{lat2}, {long2}"
    url3 = "&key=AIzaSyAGAjAGWOVhufu1j3YkkN8iVo0vmhzLMtI"

    url_full = url1+origin+url2+destination+url3
    output = requests.get(url_full).json()

    for obj in output['rows']:
        for data in obj['elements']:
            return data['distance']['value']


# print("hi")
# print(pathlen(29.3872013433149, 79.4596314939787,
#       29.3809099807938, 79.4686745644572))


def genDistanceMatrix(lat_lng, start_lat, start_lng):
    dist_mat = []
    for k in range(0, len(lat_lng)):
        mat = []
        # inserting starting point
        lat_lng[k].insert(0, list([start_lat, start_lng]))
        for i in range(0, len(lat_lng[k])):
            mat2 = []
            for j in range(0, len(lat_lng[k])):
                mat2.append(pathlen(
                    lat_lng[k][i][0], lat_lng[k][i][1], lat_lng[k][j][0], lat_lng[k][j][1]))
            mat.append(mat2)
        dist_mat.append(mat)

    return dist_mat
