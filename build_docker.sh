#!/bin/bash

docker build \
    --build-arg PLUGINPATH=core:simple_plugin_manager:base_api:fastapi \
    --build-arg CMD_ENTRYPOINT="uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0" \
    -t featureextractionserver:base .

docker build \
    --build-arg PLUGINPATH=core:simple_plugin_manager:base_api:fastapi:whisper:automated_speech_recognition \
    --build-arg CMD_ENTRYPOINT="uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0" \
    -t featureextractionserver:whisper .

docker build \
    --build-arg PLUGINPATH=core:simple_plugin_manager:base_api:fastapi:tesseract:optical_character_recognition \
    --build-arg CMD_ENTRYPOINT="uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0" \
    -t featureextractionserver:tesseract .

docker build \
    --build-arg PLUGINPATH=core:simple_plugin_manager:base_api:fastapi:clip_vit_large_patch14:text_embedding:zero_shot_image_classification \
    --build-arg CMD_ENTRYPOINT="uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0" \
    -t featureextractionserver:clip .

docker build \
    --build-arg PLUGINPATH=core:simple_plugin_manager:base_api:fastapi:blip2:conditional_image_captioning \
    --build-arg CMD_ENTRYPOINT="uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0" \
    -t featureextractionserver:blip2 .

docker build \
    --build-arg PLUGINPATH=core:simple_plugin_manager:base_api:fastapi:audio_diarization:blip:conditional_image_captioning:face_embedding:image_captioning:optical_character_recognition:simple_plugin_manager:vit_gpt2:automated_speech_recognition:blip2:detr_resnet101:face_recognition:image_embedding:owl_vit_base_patch32:tesseract:whisper:base_api:clip_vit_large_patch14:easy_ocr:fastapi:object_detection:pyannote:text_embedding:zero_shot_image_classification \
    --build-arg CMD_ENTRYPOINT="uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0" \
    -t featureextractionserver:full .

# if ((BASH_VERSINFO[0] < 4)); then
#     echo "Bash version 4.0 or higher is required."
#     exit 1
# fi

# declare -A targets
# targets["base"]="simple_plugin_manager:base_api:fastapi"
# targets["full"]="audio_diarization:blip:conditional_image_captioning:face_embedding:image_captioning:optical_character_recognition:simple_plugin_manager:vit_gpt2:automated_speech_recognition:blip2:detr_resnet101:face_recognition:image_embedding:owl_vit_base_patch32:tesseract:whisper:base_api:clip_vit_large_patch14:easy_ocr:fastapi:object_detection:pyannote:text_embedding:zero_shot_image_classification"
# targets["clip"]="simple_plugin_manager:image_embedding:base_api:clip_vit_large_patch14:fastapi:text_embedding:zero_shot_image_classification"
# targets["blip2"]="simple_plugin_manager:image_captioning:base_api:blip2:fastapi:conditional_image_captioning"
# targets["whisper"]="simple_plugin_manager:base_api:whisper:fastapi:automated_speech_recognition"
# targets["tesseract"]="simple_plugin_manager:base_api:tesseract:fastapi:optical_character_recognition"

# # Function to build a Docker image for a given target
# build_image() {
#     local target=$1

#     # Check if the target exists in the array
#     if [[ -z ${targets[$target]} ]]; then
#         echo "Error: Target '$target' is not defined in the targets array."
#         return 1  # Exit the function with an error status
#     fi

#     local pluginpath=${targets[$target]}
#     echo "Building image for $target with plugins from $pluginpath"

#     # debug why target is 0 instead of base
#     echo "target: $target"

#     # Build the Docker image using the specified PLUGINPATH
#     docker buildx build --build-arg PLUGINPATH="$pluginpath" -t "featureextractionserver:$target" .
# }

# # Build images for all defined targets
# for target in "${!targets[@]}"; do
#     build_image "$target"
# done
