#!/bin/bash

DOCKER_USERNAME="${1:-$DOCKER_USERNAME}"
VERSION="${2:-$VERSION}"

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

# Building open clip image
build_image "open_clip_vit_b32" \
    "core:simple_plugin_manager:base_api:fastapi:open_clip_vit_b32:text_embedding:zero_shot_image_classification:image_embedding" \
    "run-fes --port 8888 --host 0.0.0.0"

# Building dino image
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