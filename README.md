# Feature Extraction Server

This server can accept various media as input and performs various AI tasks, such as image captioning. It features an extensible plugin system that allows new tasks and models to be easily added. The purpose of this server is to maintain a uniform input / output specification for each AI task, regardless of the specifics of the model used. This allows models to be swapped more easily.

## Manually Install the Server

This is the recommended way to install the server.

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
   Remember that for a model to be usable at least one task plugin must also be installed. (For example text-embedding may be installed to use open-clip-vit-b32.)
6. **Run the Server**
   ```bash
   run-fes --port 8888
   ```

## Run the Server from Source

This is the recommended way to install the server if you are developing the FES.

1. **Clone the Repository**
2. **Install Python 3.11**
3. **Install the Required Packages:**
    ```bash
    pip install -r dev_requirements.txt
    ```
    Note: This includes all the dependencies for all plugins, so this can take a while. Alternatively, you can only install the dependencies you require as needed. (Check the pyproject.toml files of the plugins you need.)
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

## Run the Server with Docker

NOTE: currently, the vitrivr username on docker hub does not have the correct images. Use the faberf username instead.

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
   sudo docker run -it -p 5000:8888 -v ~/.cache:/root/.cache -v ./logs:/app/logs -e LOG_LEVEL=DEBUG -t vitrivr/featureextractionserver:full
   ```
   
   This command will start a Docker container from the image and map port 5000 of your machine to port 5000 of the Docker container. This also demonstrates how you can bind the `/root/.cache` directory to your local `.cache` directory in order to persist the downloaded machine learning models between runs, saving time.

4. **Access the Server:**

   You should now be able to access the server at `http://localhost:5000`. If you are using Docker Toolbox (generally for older systems), the Docker IP will likely be something other than `localhost`, typically `192.168.99.100`. In this case, the server will be accessible at `http://192.168.99.100:5000`.

Note: To stop the Docker container, press `CTRL | C` in the terminal window. If that does not work, open a new terminal window and run `docker ps` to get the `CONTAINER_ID`, and then run `docker stop CONTAINER_ID` to stop the container. 

Note: If the server crashes, then it likely ran out of memory. If you're running on Docker Desktop, you can increase the memory allocated to Docker in Docker's preferences:
   - For Mac: Docker menu > Preferences > Resources > Memory
   - For Windows: Docker menu > Settings > Resources > Memory

32 GB is a good amount. This will only work if your host machine has enough free memory.



## Configuring the Server

Settings can be set using either a command line argument (CLA) an environment variable (EV) or an `.env` file (EF). 

The following settings come from the core plugin.

| Name                  | Command Line Argument   | Description                                                                     |
|-----------------------|-------------------------|---------------------------------------------------------------------------------|
| LOG_LEVEL             | --log-level             | The log level. Must be one of ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] |
| LOG_PATH              | --log-path              | The path to the log file.                                                       |
| DEFAULT_CONSUMER_TYPE | --default-consumer-type | The default consumer type. Must be one of ['single_thread_consumer']            |

Additional settings may be defined or required in other plugins.


## Extending the Server

The server is extensible through plugins.

For creating new plugins which use the extraction backend to create new interfaces (such as CLIs etc), see [here](src/core/README.md).

For creating new plugins which add new endpoints to the REST API, see the fast api plugin [readme](src/fastapi/).

For creating new tasks, see [here](src/core/README.md).

For creating new models, see [here](src/core/README.md).


## Using the Server

- See [this](src/fastapi/README.md) page for more information on configuring the FastAPI REST server
- [This](src/base_api/README.md) plugin extends the server with endpoints that allow the user to create new jobs and get results.
- [This](src/legacy_api/README.md) plugin defines simpler endpoints that allow the user to both create new jobs and get results in a single call.


## Tasks

Installing these plugins adds tasks to the server which can be accessed through a variety of interfaces (see above). To properly use them, compatible models must also be installed.

- [Audio Diarization](src/audio_diarization/README.md)
- [Automated Speech Recognition](src/automated_speech_recognition/README.md)
- [Conditional Image Captioning](src/conditional_image_captioning/README.md)
- [Face Embedding](src/face_embedding/README.md)
- [Image Captioning](src/image_captioning/README.md)
- [Image Embedding](src/image_embedding/README)
- [Object Detection](src/object_detection/README.md)
- [Optical Character Recognition](src/optical_character_recognition/README.md)
- [Text Embedding](src/text_embedding/README.md)
- [Text Query Embedding](src/text_query_embedding/README.md)
- [Zero Shot Image Classification](src/zero_shot_image_classification/README)







<!-- ### Object Detection

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
- owlvit_base_patch32 -->


```
## TODO Accounts
