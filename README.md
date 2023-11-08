# Feature Extraction Server

This server can accept various media as input and performs various AI tasks, such as image captioning. It features an extensible plugin system that allows new tasks and models to be easily added. The purpose of this server is to maintain a uniform input / output specification for each AI task, regardless of the specifics of the model used. This allows models to be swapped more easily.

## Run the Development Server from Source

1. **Clone the Repository**
2. **Install Python 3.11**
3. **Install the Required Packages:**
    ```bash
    pip install -r dev_requirements.txt
    ```
    Note: This includes all the dependencies for all plugins, so this can take a while. Alternatively, you can only install the dependencies you require as needed.
4. **Run the Server:**

    To run the server in development, simply run dev_server.py:

    ```bash
    python dev_server.py
    ```
## Manually Install the Server

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
   pip install gunicorn
   ```
7. **Run the Server**
   ```bash
   gunicorn -w ${NUMBER_OF_WORKERS} -b :5000 --timeout 600 --preload 'feature_extraction_server.flask.entrypoint:entrypoint()'
   ```

## Run the Server with Docker

Follow these steps to run the server using Docker:

1. **Install Docker:**

   You need to have Docker installed on your machine. You can download Docker Desktop for Mac or Windows [here](https://www.docker.com/products/docker-desktop). For Linux users, Docker Engine is the appropriate version, and the installation instructions vary by distribution.

2. **Pull the Docker Image:**

   Pull the Docker image from Docker Hub with the following command:

   ```bash
   docker pull faberf/featureextractionserver
   ```

3. **Run the Docker Image:**

   After pulling the image, you can run it using the following command:

   ```bash
   docker run -it -p 5000:5000 faberf/featureextractionserver
   ```
   
   This command will start a Docker container from the image and map port 5000 of your machine to port 5000 of the Docker container. Keep in mind that the Docker image contains all current plugins and is thus somewhat bloated. Optionally you can bind the `/root/.cache` directory to your local `.cache` directory in order to persist the downloaded machine learning models between runs (this saves time).

   ```bash
   docker run -it -p 5000:5000 -v ~/.cache:/root/.cache faberf/featureextractionserver
   ```

   Note: If the server crashes, then it may be because it ran out of memory. If you're running on Docker Desktop, you can increase the memory allocated to Docker in Docker's preferences:
   - For Mac: Docker menu > Preferences > Resources > Memory
   - For Windows: Docker menu > Settings > Resources > Memory

## Build a Custom Docker Image

If you would like to profit from the convenience and reproduceability of Docker, but you would like to customize which plugins are included in the image, you can build your own image.

1. **Copy all the Required Plugins into `plugins_to_install`**
2. **Build the Image**

    in the root directory:
    ```bash 
    docker build -t example_image_name .
    ```
3. **Run the Image**
   
   See the instructions above, replacing `faberf/featureextractionserver` with your image name.


## Configuring the Server

Settings can be set using either a command line argument (CLA) an environment variable (EV) or an `.env` file (EF). 


| Setting | Description | Default| Dev Server | Gunicorn | Docker |
|-|-|-|-|-|-|
|LOG_LEVEL|Either `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`| `INFO`| CLA EV EF | EV EF | EV EF |
|LOG_PATH|Where the log file is stored| `logs/log.txt`| CLA EV EF | EV EF | EV EF |
|HOST|Used to specify a host for the development server| `localhost`| CLA EV EF | - | - |
|PORT|Used to specify a port for the development server | 5000 | CLA EV EF | - | - |
|RESULT_CHECK_INTERVAL|The interval in seconds between checks for the result of a job| 0.1| CLA EV EF | EV EF | EV EF |
|DEFAULT_TASK|The default task which the system assumes if the task cannot be inferred otherwise| -| CLA EV EF | EV EF | EV EF |
|DEFAULT_MODEL_{task}|These settings determine the default model which the system assumes if the task is known but the model cannot be inferred otherwise|-| CLA EV EF | EV EF | EV EF |
|DEFAULT_CONSUMER_TYPE|The default consumer type for models which do not specify a type| `single_thread_consumer`| CLA EV EF | EV EF | EV EF |
|NUMBER_OF_WORKERS|The number of gunicorn workers|1|-|EV|EV|

## Extending the Server

The server is extensible through plugins. The core system uses namespace packages to discover modules from plugins. There are four namespaces:

1. `apis`
   
   An api module must implement `add_routes(application_interface, flask_app)` and optionally `add_settings(settings_manager)`
2. `models`
   
   A model module must implement `load_model` and optionally `add_settings(settings_manager)`. In addition it may implement any task (naming a global function the same as a task). The consumer type can be set with a global string variable `consumer_type`.
3. `tasks`
   
   A task module must implement the function `wrap(func)` which is a decorator intended to perform pre- and postprocessing steps that are relevant for any implementation of the task.
4. `consumers`
    
    A consumer module must implement `start(model, log_server)`



## Task and Model Plugins

### Image Captioning

This task allows you to generate a text caption that describes the visual content of an image. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `image` | Yes | The image that needs captioning |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a list of strings that caption the image (typically with only one element). In **Batch Mode**, if the 'image' key is set to a list of strings, the task will return a list of lists (one list for each image in the input).

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

The task responds with a list of strings that caption the image (typically with only one element). These strings do not include the specified prefix. In **Batch Mode**, if the 'image' or 'text' key is set to a list of strings, the task will return a list of lists (one list for each image / text in the input).

To use this task, at least one compatible model plugin must be installed: 
- blip
- blip2

### Automated Speech Recognition

This task allows you to generate text from speech. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `audio` | Yes | The audio from which the speech needs to be generated |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a string of recognized audio. In  **Batch Mode**, if the 'audio' key is set to a list of strings, the task will return a list of strings.

To use this task, at least one compatible model plugin must be installed: 
- whisper

### Zero Shot Image Classification

This task allows you to to match an image to a class from a catalogue of classes. The task requires input with the specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `image` | Yes | The image that needs to classified |
|`classes` | Yes | A list of strings that represents the catalogue of classes |
| `config` | No | Any additional arguments (depending on the model) |

The task responds with a list of floating point numbers between 0 and 1 that represent the probability that the image belongs to a class. In **Batch Mode**, if the 'image' key is set to a list of strings, the task will return a list of lists (one list for each image in the input).

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


### Base API

- **GET** `/api/tasks/list`: List all available tasks.
- **GET** `/api/models/list`: Retrieve a list of all available models.
- **GET** `/api/models/<model>/tasks/list`: List all tasks available for a specific model.
- **GET** `/api/tasks/<task>/models/list`: Get all models that are capable of performing a specified task.
- **POST** `/api/models/<model>/tasks/<task>/features`: Extract features by executing a task-model combination.
  - alternatively `/api/tasks/<task>/models/<model>/features` 
  - alternatively `/api/tasks/<task>/features` (where the server uses a configured default model)
  - The payload should be a json string which encodes the input for the task. 
  - Images are encoded base64. Optionally, the encoded string can have a data URL prefix (e.g., `data:image/png;base64,iVBORw0KGgoA...`)

- **POST** `/api/models/<model>/start`: Send a request to load and start a model in advance.
- **POST** `/api/models/<model>/stop`: Send a request to stop a model.

### Legacy API

The previous API with "extract" endpoint. For details, see previous versions of this readme.