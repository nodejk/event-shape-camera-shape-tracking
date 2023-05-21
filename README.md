# Event Camera Shape Tracking

## How to run the pipeline:

Note: You have to create a Sessions folder under DBSCAN and GSCEventMOD in order to save the pipeline output.

1. Run the following command in the CLI to run GSC event mod configuration:

```bash
python3 main.py --config gsceventmod-config.json
```

2. Run the following command in the Cli to run DBScan implementation:

```bash
python3 main.py --config dbscan-config.json
```

---

## Understanding configuration for the pipeline.

Every step in the clustering pipeline is represented with a help of a class and are validated on the fly 
from the configuration json file using Configuration.py.

**parameters** defined under model_parameters are passed to the model defined above it. 

```
{
  "model": "DBScan",
  "model_parameters" : {
        "parameters": {
            "eps": 50,
            "min_samples": 10,
            "algorithm": "auto",
            "metric": "euclidean"
        }
  },
  ...
}
```



### Event Data Processors
Steps represents the types of data processes to be initialized on the event data and later on run on the data before 
converting the events to binary images and passing it to Data Processor Steps.

**name**: is the folder name under EventDataProcessors. <br>
**parameters**: parameters passed to the particular method.


```
"event_data_processors": {
    "steps": [
        {
            "name": "isolation_forest",
            "parameters": {
                "random_state": 0,
                "contamination": 0.3
            }
        }
    ]
},
```

### Data Processors
Steps represents the types of data processors to be initialized and later on run on the data
before passing it to the Data Transformer Steps.
```
{
    "data_processors": {
        "steps": [
            {
                "name": "median_filter",
                "parameters": {
                    "size": 3
                }
            }
        ]
   }
}
```

### Data Transformers
Finally, after processing the event data and the image data, the data is finally transformed (say, converting the range 
of input not implemented here) and passed to the model for clustering.

```
"data_transformers": {
    "steps": []
}
```

### Saving and Visualizing Model Output

**save**: if true, creates a folder under model/Sessions from hash and saves the configuration as config.json and image 
output to model_output folder.

**display**: if true, displays the output of the model in a window.

```
"model_output": {
    "save": false,
    "display": true
}
```

### Event Source

**source_type**: if "file", then parameters take an attribute known as file_path (str) which is the source file path of 
the Aedat file. else if "live", then takes, address (str), port (int), height (int) and width (int) of the event being 
streamed from the event camera.

```
"events_input": {
    "source_type": "file",
    "parameters": {
        "file_path": "./Cars_sequence.aedat4"
    }
}
```

---
## 

The pipeline runs with the help of a validation config.json file as it allows to manipulate the pipeline
accordingly by modifying the clustering model, data processors, data transformers, event data processors 
and the input of the model.

A sample dbscan-config.json and gsceventmod-config is provided in the repo to test out.

---
## Contribution Guidelines

To implement a new clustering method, create a new folder with the model name and create the following files and folder:

```
__init__.py
ModelName.py
/Sessions
```
implement class Pipeline in `__init__.py` and run all the required in the pipeline in the same (say, initializing data processors etc)

extend class ClusteringModel to ModelName in `ModelName.py`.


## ToDo

1. Remove static implementation of kalman filter and make it configurable using config.json.
2. Add new models to experiment clustering.
