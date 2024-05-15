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
   export PYTHONPATH=src/core:src/legacy_api:src/audio_diarization:src/blip:src/conditional_image_captioning:src/face_embedding:src/image_captioning:src/optical_character_recognition:src/simple_plugin_manager:src/vit_gpt2:src/automated_speech_recognition:src/blip2:src/detr_resnet101:src/face_recognition:src/image_embedding:src/owl_vit_base_patch32:src/tesseract:src/whisper:src/base_api:src/clip_vit_large_patch14:src/easy_ocr:src/fastapi:src/object_detection:src/pyannote:src/text_embedding:src/zero_shot_image_classification:$PYTHONPATH
   export LOG_LEVEL=DEBUG

   ```
5. **Run the Server:**

    To run the server, use the entrypoint:

    ```bash
   python run_dev_server.py --port 8888
    ```
## Manually Install the Server

This is currently not tested.

1. **Clone the Repository**
2. **Install Python 3.11**
3. **Install Flit**
   
   ```bash
   python3 -m pip install flit
   ```
4. **Install the Core Project and some core plugins**
   ```bash
   cd src/core
   flit install
   cd ../simple_plugin_manager
   flit install
   cd ../fastapi
   flit install
   cd ../base_api
   flit install
   ```
5. **Install any desired Plugins**
   ```bash
   cd src/example_plugin
   flit install
   ```
6. **Run the Server**
   ```bash
   run-fes --port 8888
   ```

## Run the Server with Docker

Follow these steps to run the server using Docker:


1. **Install Docker:**

   You need to have Docker installed on your machine. You can download Docker Desktop for Mac or Windows [here](https://www.docker.com/products/docker-desktop). For Linux users, Docker Engine is the appropriate version, and the installation instructions vary by distribution.

2. **Build or Pull the Docker Image:**

   The dockerfile requires the build arguments PLUGINPATH and CMD_ENTRYPOINT to build an image. 
   
   ```bash
       docker buildx build \
        --platform linux/amd64,linux/arm64,linux/arm/v7 \
        --build-arg PLUGINPATH="core:simple_plugin_manager:base_api:fastapi" \
        --build-arg CMD_ENTRYPOINT="run-fes --port 8888 --host 0.0.0.0" \
        --tag "featureextractionserver:my_custom_tag" \
        --push \
        .
   ```

   You can check build_docker.sh for more examples. Alternatively you can use a prebuilt image from docker hub. Choose a tag from docker hub https://hub.docker.com/r/vitrivr/featureextractionserver/tags. For example, if you want to have pull an image from Docker hub with all plugins installed, use the following command:

   ```bash
   docker pull vitrivr/featureextractionserver:full
   ```

3. **Run the Docker Image:**

   After pulling the image, you can run it using the following command:

   ```bash
   sudo docker run -it -p 5000:8888 -v ~/.cache:/root/.cache -v ./logs:/app/logs -e LOG_LEVEL=DEBUG -t faberf/featureextractionserver:full
   ```
   
   This command will start a Docker container from the image and map port 5000 of your machine to port 5000 of the Docker container. This also demonstrates how you can bind the `/root/.cache` directory to your local `.cache` directory in order to persist the downloaded machine learning models between runs, saving time.

4. **Access the Server:**

   You should now be able to access the server at `http://localhost:5000`. If you are using Docker Toolbox (generally for older systems), the Docker IP will likely be something other than `localhost`, typically `192.168.99.100`. In this case, the server will be accessible at `http://192.168.99.100:5000`.

Note: To stop the Docker container, press `CTRL + C` in the terminal window. If that does not work, open a new terminal window and run `docker ps` to get the `CONTAINER_ID`, and then run `docker stop CONTAINER_ID` to stop the container. 

Note: If the server crashes, then it likely ran out of memory. If you're running on Docker Desktop, you can increase the memory allocated to Docker in Docker's preferences:
   - For Mac: Docker menu > Preferences > Resources > Memory
   - For Windows: Docker menu > Settings > Resources > Memory

32 GB is a good amount. This will only work if your host machine has enough free memory.



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