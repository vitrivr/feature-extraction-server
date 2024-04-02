# Feature Extraction Server

This server can accept various media as input and performs various AI tasks, such as image captioning. It features an extensible plugin system that allows new tasks and models to be easily added. The purpose of this server is to maintain a uniform input / output specification for each AI task, regardless of the specifics of the model used. This allows models to be swapped more easily.

## Run the Server from Source

1. **Clone the Repository**
2. **Install Python 3.11**
3. **Install the Required Packages:**
    ```bash
    pip install -r dev_requirements.txt
    ```
    Note: This includes all the dependencies for all plugins, so this can take a while. Alternatively, you can only install the dependencies you require as needed.
4. **Add the Desired Plugins to the Path**
   For example:
   ```bash
   export PYTHONPATH=feature_extraction_server-core:plugins/simple_plugin_manager:plugins/feature_extraction_server-models-clip_vit_large_patch14:plugins/feature_extraction_server-services-base_api:plugins/feature_extraction_server-services-fastapi:plugins/feature_extraction_server-tasks-image_embedding:plugins/feature_extraction_server-tasks-text_embedding:$PYTHONPATH
   export LOG_LEVEL=DEBUG

   ```
5. **Run the Server:**

    To run the server, use uvicorn:

    ```bash
    uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888
    ```
## Manually Install the Server

This is currently not tested.

1. **Clone the Repository**
2. **Install Python 3.11**
3. **Install Flit**
   
   ```bash
   python3 -m pip install flit
   ```
4. **Install the Core Project**
   ```bash
   cd feature_extraction_server-core
   flit install
   ```
5. **Install any desired Plugins**
   ```bash
   cd plugins/feature_extraction_server-example_plugin
   flit install
   ```
6. **Install Gunicorn**
   ```bash
   pip install uvicorn
   ```
7. **Run the Server**
   ```bash
   uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888
   ```

## Run the Server with Docker

TODO


## Configuring the Server

Settings can be set using either a command line argument (CLA) an environment variable (EV) or an `.env` file (EF). 

TODO

## Extending the Server

The server is extensible through plugins. The core system uses namespace packages to discover modules from plugins. There are four namespaces:

TODO



## Task and Model Plugins

### Image Captioning

This task allows you to generate a text caption that describes the visual content of an image. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `image` | Yes | The image that needs captioning |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a string that captions the image.

To use this task, at least one compatible model plugin must be installed: 
- blip
- blip2
- vit_gpt2



### Conditional Image Captioning

This task allows you to use a text prompt to condition an image captioning task. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `image` | Yes | The image that needs captioning |
|`text` | Yes | A specified prefix for the caption that should be generated. For example `"Question: What is depicted in this photograph? Answer:"` |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a string that captions the image.

To use this task, at least one compatible model plugin must be installed: 
- blip
- blip2

### Automated Speech Recognition

This task allows you to generate text from speech. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `audio` | Yes | The audio from which the speech needs to be generated |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a string of recognized audio.

To use this task, at least one compatible model plugin must be installed: 
- whisper

### Zero Shot Image Classification

This task allows you to to match an image to a class from a catalogue of classes. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `image` | Yes | The image that needs to classified |
|`classes` | Yes | A list of strings that represents the catalogue of classes |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a list of floating point numbers between 0 and 1 that represent the probability that the image belongs to a class.

To use this task, at least one compatible model plugin must be installed: 
- clip_vit_large_patch14

### Object Detection

This task allows you to identify regions of an image that contain objects. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `image` | Yes | The image in which objects need to be detected |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a dictionary that includes the keys `boxes`, `labels`, `scores`. Each key maps to a list of the same length: the number of detected objects. An item in the `boxes` list is a list with four values (xmin, ymin, xmax, ymax), an item in the `labels` list is the name of the object as a string, an item in the `scores` list is a floating point number between 0 and 1 which represents the confidence that the object was detected correctly. Here is an example:


```json
{
  "boxes": [
    [30, 50, 200, 300],
    [10, 20, 100, 200],
    [300, 400, 500, 600]
  ],
  "labels": [
    "cat",
    "dog",
    "bird"
  ],
  "scores": [
    0.95,
    0.85,
    0.78
  ]
}
```

To use this task, at least one compatible model plugin must be installed: 
- owlvit_base_patch32

## API Plugins

TODO

Go to /docs to see the API endpoints.