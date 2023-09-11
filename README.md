# Feature Extraction Server

This server can accept various media as input and performs various AI tasks, such as image captioning. It uses a modular design that allows new tasks and models to be easily added. The purpose of this server is to maintain a uniform input / output specification for each AI task, regardless of the specifics of the model used. This allows models to be swapped more easily.


## Server Side

### Run the Server from Source

1. **Clone the Repository**
2. **Install Python 3.11**
3. **Install the Required Packages:**
    ```bash
    pip install -r environment.txt
    ```
4. **Run the Server:**

    To run the server in development, simply run dev_server.py:

    ```bash
    python dev_server.py
    ```

    Otherwise use a WSGI server such as gunicorn:

    ```bash
    pip install gunicorn
    gunicorn -b :5000 --timeout 600 --preload 'feature_extraction_server.app:entrypoint()'
    ```
    Make sure to set the timeout very long, since the first time a model executes it may need to download many files.

The server will start running on localhost on port 5000.


### Run the Server with Docker

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
   docker run -it -e WORKERS=1 -p 5000:5000 faberf/featureextractionserver
   ```
   
   This command will start a Docker container from the image and map port 5000 of your machine to port 5000 of the Docker container. Optionally you can bind the `/root/.cache` directory to your local `.cache` directory in order to persist the downloaded machine learning models between runs (this saves time).

   ```bash
   docker run -it -e WORKERS=1 -p 5000:5000 -v ~/.cache:/root/.cache faberf/featureextractionserver
   ```

4. **Access the Server:**

   You should now be able to access the server at `http://localhost:5000`. If you are using Docker Toolbox (generally for older systems), the Docker IP will likely be something other than `localhost`, typically `192.168.99.100`. In this case, the server will be accessible at `http://192.168.99.100:5000`.

Note: To stop the Docker container, press `CTRL + C` in the terminal window. If that does not work, open a new terminal window and run `docker ps` to get the `CONTAINER_ID`, and then run `docker stop CONTAINER_ID` to stop the container. 

Note: If the server crashes, then it likely ran out of memory. If you're running on Docker Desktop, you can increase the memory allocated to Docker in Docker's preferences:
   - For Mac: Docker menu > Preferences > Resources > Memory
   - For Windows: Docker menu > Settings > Resources > Memory

32 GB is a good amount. This will only work if your host machine has enough free memory.

### Configuring the Server

- Log Level
  - Either `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  - Command line argument `--log-level` available for development server
  - Otherwise, set the environment variable `LOG_LEVEL`
  - TODO: environment file
  - Default is `INFO` as specified in the settings module
- Log Path
  - Where the log file is stored
  - Command line argument `--log-path` available for development server
  - Otherwise, set the environment variable `LOG_PATH`
  - TODO: environment file
  - Default is `default.log` as specified in the settings module
- Default Task
  - When no task is specified in a request, this setting is used
  - Command line argument `--default-task` available for development server
  - Otherwise, set the environment variable `DEFAULT_TASK`
  - TODO: environment file
  - Default is `image_captioning` as specified in the settings module
- Port
  - Used to specify a port 
  - For the development server:
    - Command line argument `--port` or `-p`
    - Otherwise set the environment variable `PORT`
    - TODO: environment file
    - Default is `5000` as specified in app module
   - For the Docker Image:
      Use docker compose or docker run to route port 5000 to your desired port


## Client Side

To perform an AI Task, send a POST request to the `/extract` endpoint with a JSON body. The JSON should have the key 'task' set to the intended task and any additional data required to execute the task. It can optionally contain 'model' to specify the model, and 'config' to specify any additional arguments. 

Here is an example of how to caption an image using a curl command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image": "<base64-encoded-image>", "task": "image_captioning", "model": "blip", "config": {"top_k":50}}' http://localhost:5000/extract
```

this returns 

```json
["a black and white photo of a house"]
```

### Image Captioning

This service allows you to generate a text caption that describes the visual content of an image. The API requires a JSON body with specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `task` | Yes | This should be set to `image_captioning` |
| `image` | Yes | A base64 encoded image string. Optionally, the encoded string can have a data URL prefix (e.g., `data:image/png;base64,iVBORw0KGgoA...`) |
| `model` | No | The model which should execute the captioning |
| `config` | No | Any additional arguments (depending on the model) |

The API responds with a list of strings that caption the image. Typically, this list will contain one item, but depending on the model and configuration used, it may contain multiple items. In **Batch Mode**, if the 'image' key is set to a list of strings, the server will return a list of lists (one list for each image in the input).




### Conditional Image Captioning

This service allows you to use a text prompt to condition an image captioning task. The API requires a JSON body with specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `task` | Yes | This should be set to `conditional_image_captioning` |
| `image` | Yes | A base64 encoded image string. Optionally, the encoded string can have a data URL prefix (e.g., `data:image/png;base64,iVBORw0KGgoA...`) |
|`text` | Yes | A specified prefix for the caption that should be generated. For example `Question: What is depicted in this photograph? Answer:` |
| `model` | No | The model which should execute the captioning |
| `config` | No | Any additional arguments (depending on the model) |

The API responds with a list of strings that caption the image. These strings do not include the specified prefix. In **Batch Mode**, if the 'image' or 'text' key is set to a list of strings, the server will return a list of lists (one list for each image / text in the input).


### Automated Speech Recognition

This service allows you to generate text from speech. The API requires a JSON body with specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `task` | Yes | This should be set to `automated_speech_recognition` |
| `audio` | Yes | A base64 encoded audio. Optionally, the encoded string can have a data URL prefix (e.g., `data:audio/wav;base64,iVBORw0KGgoA...`) |
| `model` | No | The model which should execute the speech recognition |
| `config` | No | Any additional arguments (depending on the model) |

The API responds with a string of recognized audio. In  **Batch Mode**, if the 'audio' key is set to a list of strings, the server will return a list of strings.

### Zero Shot Image Classification

This service allows you to to match an image to a class from a catalogue of classes. The API requires a JSON body with specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `task` | Yes | This should be set to `zero_shot_image_classification` |
| `image` | Yes | A base64 encoded image string. Optionally, the encoded string can have a data URL prefix (e.g., `data:image/png;base64,iVBORw0KGgoA...`) |
|`classes` | Yes | A list of strings that represents the catalogue of classes |
| `model` | No | The model which should execute the classification |
| `config` | No | Any additional arguments (depending on the model) |

The API responds with a list of floating point numbers between 0 and 1 that represent the probability that the image belongs to a class. In **Batch Mode**, if the 'image' key is set to a list of strings, the server will return a list of lists (one list for each image in the input).

### Object Detection

This service allows you to identify regions of an image that contain objects. The API requires a JSON body with specific keys:

| Key | Required | Description |
| --- | --- | --- |
| `task` | Yes | This should be set to `object_detection` |
| `image` | Yes | A base64 encoded image string. Optionally, the encoded string can have a data URL prefix (e.g., `data:image/png;base64,iVBORw0KGgoA...`) |
| `model` | No | The model which should execute the object detection |
| `config` | No | Any additional arguments (depending on the model) |

The API response with a dictionary that includes the keys `boxes`, `labels`, `scores`. Each key is maps to a list of the same length, the number of detected objects. An item in the `boxes` list is a list with four values (xmin, ymin, xmax, ymax), an item in the `labels` list is the name of the object as a string, an item in the `scores` is a floating point number between 0 and 1 which represents the confidence that the object was detected correctly.

## Extending the Server

The server is designed to be easily extensible with new tasks and models. To add a new task or model, follow these steps:

1. **Add a new task**: To add a new task, edit the tasks module so that it implements a wrapper function. Make sure you also update the `tasks` dictionary and the `default_models` dictionary (also in the tasks module).

2. **Add a new model**: To add a new model, simply add a new Python file in the models directory. For each task that this model is able to do you can implement a function that is named after the task.

For example, if you want to add a new audio classification model, you might create a new file called 'cool_model.py'. In 'cool_model.py', you would define your classification function like this:

```python
def audio_classification(image, other_arg, more_args):
    # Your model's audio classification code here
    pass
```
Of course, make sure to edit the tasks module if the task 'audio_classification' does not exist yet. 
After these steps, you can specify 'audio_classification' as the task and 'cool_model' as the model in your POST request to the /extract endpoint.

## API Endpoints

- **POST /extract**: Perform extraction with the specified task (or default task) and model (or default model). All other arguments will be passed to the task wrapper which wraps the models functions.
- **POST /load**: Load a model (or default model) in advance.
- **POST /free**: Free memory from a model (or default model).
- **GET /tasks**: Get a list of all available tasks.
<!-- 
- **GET /models/\<task>**: Get a list of all models available for the specified task. -->