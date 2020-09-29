import os
import json
import math
import glob
import pandas as pd
import numpy as np

#Builds dictionary recursively using a template.
def dic_builder(data, structure, ref):
    aux = data
    if len(structure["filter"]) != 0:
        aux = data.loc[data[structure["tag"]] == structure["filter"][ref]]
    if structure["contentType"] == "JSON":
        result = {}
        if structure["content"]["name"] == "UNIQUE_GENERATED":
            for key in sorted(aux[structure["content"]["tag"]].unique()):
                result.update({str(key): dic_builder(aux.loc[aux[structure["content"]["tag"]] == key], structure["content"], ref)})
    elif structure["contentType"] == "Array":
        result = []
        for i in data[structure["content"]["tag"]]:
            result.append(i)
    elif structure["contentType"] == "float":
        result = 0.0
        for i in data[structure["content"]["tag"]]:
            if math.isnan(i):
                continue
            result += i
    elif structure["contentType"] == "int":
        result = 0
        for i in data[structure["content"]["tag"]]:
            if math.isnan(i):
                continue
            result += i
        result = int(result)
    return result

#Merges the content of two dictionaries, only numerical values 
def dicJoin(d1, d2, keyIgnore):
    for key in d2.keys():
        if key in keyIgnore:
            continue
        if key in d1.keys():
            if type(d2[key]) is int or type(d2[key]) is float:
                d1[key] = d1[key] + d2[key]
            elif type(d2[key]) is str:
                d1[key] = d1[key]
            else:
                d1[key] = dicJoin(d1[key], d2[key], keyIgnore)
        else:
            d1.update({key:d2[key]})
            continue
    return d1

#Merges the content of a list of dictionaries, ignoring some keys.
def merge_Dic(dic_list, keyIgnore):
    dic = {}
    dic.update(dic_list[0])
    for d in dic_list[1:]:
        dic = dicJoin(dic, d, keyIgnore)
    return dic

#Creates Folders for the output files
def createFolders(output):
    os.makedirs(os.path.join(output), exist_ok=True)
    os.makedirs(os.path.join(output,"Nodes"), exist_ok=True)
    os.makedirs(os.path.join(output,"Edges"), exist_ok=True)

#Node processing function
def node_processing(data, node_template, output):
    nodeFile = open(node_template, )
    nodeT = json.load(nodeFile)
    nodeFile.close()
    nodes = []
    for tag in nodeT["nodeID"]:
        nodes = sorted(np.unique(nodes+list(data[tag].unique())))
    for node in nodes:
        list_of_dic = []
        if nodeT["IDType"] == "String":
            nodeID = str(node)
        elif  nodeT["IDType"] == "int":
            if math.isnan(node):
                continue
            nodeID = int(node)
        for i in range(len(nodeT["nodeID"])):
            dic = {}
            dic.update({"nodeID": nodeID})
            aux = data.loc[data[nodeT["nodeID"][i]] == node]
            for key in nodeT["structure"].keys():
                dic.update({nodeT["structure"][key]["name"]: dic_builder(aux, nodeT["structure"][key], i)})
            list_of_dic.append(dic)
        dic  = merge_Dic(list_of_dic, ["nodeID"])
        with open(os.path.join(output, "Nodes", "{}.json".format(dic["nodeID"])), 'w+') as nodeFile:
            nodeFile.write(json.dumps(dic, indent=4))

#Edge processing function
def edge_processing(data, edge_template, output):
    edgeFile = open(edge_template, )
    edgeT = json.load(edgeFile)
    edgeFile.close()
    for i in data.index:
        dic = {}
        aux= data.loc[[i]]
        #EdgeHead definition
        if edgeT["headType"] == "int":
            if math.isnan(aux[edgeT["edgeHead"]]):
                continue
            dic.update({"edgeHead" : int(aux[edgeT["edgeHead"]])})
        elif edgeT["headType"] == "float":
            if math.isnan(aux[edgeT["edgeHead"]]):
                continue
            dic.update({"edgeHead" : float(aux[edgeT["edgeHead"]])})
        else:
            dic.update({"edgeHead" : str(aux[edgeT["edgeHead"]])})
        #EdgeTail definition
        if edgeT["tailType"] == "int":
            if math.isnan(aux[edgeT["edgeTail"]]):
                continue
            dic.update({"edgeTail" : int(aux[edgeT["edgeTail"]])})
        elif edgeT["tailType"] == "float":
            if math.isnan(aux[edgeT["edgeTail"]]):
                continue
            dic.update({"tailHead" : float(aux[edgeT["edgeTail"]])})
        else:
            dic.update({"edgeTail" : str(aux[edgeT["edgeTail"]])})
        #Inversion check
        for param in edgeT["inversorTag"]:
            if param in edgeT["inversorValues"][edgeT["inversorTag"].index(param)]:
                headAux = dic["edgeHead"]
                dic.update({"edgeHead":dic["edgeTail"]})
                dic.update({"edgeTail":headAux})
                break
        #JSON Formatted line
        for key in edgeT["structure"].keys():
            dic.update({edgeT["structure"][key]["name"]: dic_builder(aux, edgeT["structure"][key], 0)})
        previous_content = {}
        if os.path.exists(os.path.join(output, "Edges", "{tail}{connec}{head}.json".format(tail=dic["edgeTail"], connec=edgeT["file_name_connector"], head=dic["edgeHead"]))):
            with open(os.path.join(output, "Edges", "{tail}{connec}{head}.json".format(tail=dic["edgeTail"], connec=edgeT["file_name_connector"], head=dic["edgeHead"])), 'r') as edgeFile:
                previous_content = json.load(edgeFile)
        with open(os.path.join(output, "Edges", "{tail}{connec}{head}.json".format(tail=dic["edgeTail"], connec=edgeT["file_name_connector"], head=dic["edgeHead"])), 'w+') as edgeFile:
            dic = merge_Dic([dic, previous_content], ["edgeHead", "edgeTail"])
            edgeFile.write(json.dumps(dic, indent=4))


#Process function
def process(data, node_template, edge_template, output):
    createFolders(output)
    try:
        #Node processing
        node_processing(data, node_template, output)
    except:
        print("Error while processing nodes")
        return 1
    try:
        #Edge processing
        edge_processing(data, edge_template, output)
    except:
        print("Error while processing edges")
        return 1
    return 0