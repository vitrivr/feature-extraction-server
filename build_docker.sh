#!/bin/bash

# Check if the buildx builder "mybuilder" already exists, if not create it
if ! docker buildx inspect mybuilder > /dev/null 2>&1; then
    docker buildx create --name mybuilder --driver docker-container --use
else
    docker buildx use mybuilder
fi

build_image() {
    local tag_suffix=$1
    local plugin_path=$2
    local entrypoint=$3

    docker buildx build \
        --platform linux/amd64,linux/arm64,linux/arm/v7 \
        --build-arg PLUGINPATH="$plugin_path" \
        --build-arg CMD_ENTRYPOINT="$entrypoint" \
        --tag "$DOCKER_USERNAME/featureextractionserver:${tag_suffix}-$VERSION" \
        --tag "$DOCKER_USERNAME/featureextractionserver:${tag_suffix}-latest" \
        --push \
        .
}

# Building base image
build_image "base" \
    "core:simple_plugin_manager:base_api:fastapi" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building base image
build_image "dino" \
    "core:simple_plugin_manager:base_api:fastapi:dino_v2_vits14:image_embedding" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building whisper image
build_image "whisper" \
    "core:simple_plugin_manager:base_api:fastapi:whisper:automated_speech_recognition" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building tesseract image
build_image "tesseract" \
    "core:simple_plugin_manager:base_api:fastapi:tesseract:optical_character_recognition" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building clip image
build_image "clip_vit_large_patch14" \
    "core:simple_plugin_manager:base_api:fastapi:clip_vit_large_patch14:text_embedding:zero_shot_image_classification:image_embedding" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building blip2 image
build_image "blip2" \
    "core:simple_plugin_manager:base_api:fastapi:blip2:conditional_image_captioning" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building full image
build_image "full" \
    "core:simple_plugin_manager:base_api:fastapi:audio_diarization:blip:conditional_image_captioning:face_embedding:image_captioning:optical_character_recognition:simple_plugin_manager:vit_gpt2:automated_speech_recognition:blip2:detr_resnet101:face_recognition:image_embedding:owl_vit_base_patch32:tesseract:whisper:base_api:clip_vit_large_patch14:easy_ocr:fastapi:object_detection:pyannote:text_embedding:zero_shot_image_classification:dino_v2_vits14" \
    "run-fes --port 8888 --host 0.0.0.0"

# Remove the buildx builder
docker buildx rm mybuilder


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
