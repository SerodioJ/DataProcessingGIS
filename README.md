# DataProcessingGIS
## Requirements
In order to use run this IPython Notebooks, [Python](https://www.python.org/) is needed (version 3.7.3 was used). 

After having python on your machine, use package manager (e.g. pip) to install all dependencies presented in [requirements.txt](requirements.txt). If using pip:
```
$ pip install -r requirements.txt
```

## Launching the Jupyter App

Use the following command:
```
$ jupyter notebook
```
After doing so, you will be able to open the notebook on your browser and see your folder and files.

## Processing Notebook
In the [Processing Notebook](Processing.ipynb), is where you can set the path to files and folders that will be used in the data processing part. A few outputs (nodes and edges JSON files) of this notebook that resulted from the [CET-SP Origin-Destination Survey Data](http://www.cetsp.com.br/consultas/pesquisa-origem-e-destino-de-cargas/a-pesquisa.aspx) can be seen in this [folder](ProcessedData/baseOD).

Note that, a few of them are templates that you will have to create according to your preferences.

### Templates
All the most external keys in the template (e.g. [node](templates/Nodes/baseOD.json) and [edge](templates/Edges/baseOD.json)) are required and its values are to be set by the user. The nested JSON in `"structure"` describes how the data will be treated in the `process` function. More detailed information about templates will be added in the future.

## Export Notebook
In the [Export Notebook](Export.ipynb), is where you can set the path to files and folders that will be used in the export part. The last cell depends on what you are looking for so it will need to be coded according to your preferences. [Example of an output from this notebook](out/baseOD/agrico.csv)

### Spatial data
You can create a JSON to use as a node dictionary (e.g. [zoning](data/baseOD/zoning.json)) and use the function `generate_JSON` to get a JSON with lat/long information (e.g. [spatial](data/baseOD/spatial.json)) 