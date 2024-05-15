# Image Embedding
This plugin adds the image embedding task (batched and non-batched) which allows you to represent visual information from image data with a dense vector.

## Installation

This plugin requires core and simple_plugin_manager as dependencies. For source, local and containerized installation instructions please see the main [README](../../README.md).

To execute the task, a plugin which includes a model that supports the image embedding task should be installed. 

Currently, the following models support image embedding:
- [CLIP ViT Large Patch 14](../clip_vit_large_patch14/README.md)
- [Dino V2 ViTs 14](../dino_v2_vits14/README.md)
- [Open CLIP ViT B32](../open_clip_vit_b32/README.md)

To expose the task as an endpoint the [fastapi](../fastapi/README.md) plugin and one of the following apis should be installed:
- [base_api](../base_api/README.md)
- [legacy_api](../legacy_api/README.md)

## Usage

As input this task requires the following fields:

| Key | Required | Batched | Type| Description |
| --- | --- | --- | --- | --- |
| `image` | Yes | Yes | image data | The image which should be embedded |
| `config` | No | Yes | dict | Any additional arguments (see the model documentation) |


As ouput this task returns the following fields:

| Key | Batched | Type| Description |
| --- | --- | --- | --- |
| `embedding` | Yes | list of floats | The embedding |

When the task is executed in batched mode, the batched fields are given (or returned) as lists, whereas the non-batched fields are given as simple values.

### Example

For the `/api/tasks/image-embedding/{model}/jobs` endpoint defined in [base_api](../base_api/README.md) the following request body serves as an example:

```json
{
  "image": "data:image/jpeg;base64,UklGRhDUCwB...",
  "config": {}
}
```

This returns:

```json
{
  "id": "05032039-e7dd-4ca5-8941-ebff9f5f2e09",
  "status": "starting"
}
```

Later, the result can be retrieved using `/api/tasks/image-embedding/jobs/05032039-e7dd-4ca5-8941-ebff9f5f2e09`:

```json
{
  "status": "complete",
  "result": {
    "embedding": [
      -3.520469903945923,
      -0.28723829984664917,
      -0.47991180419921875,
      -2.594832420349121,
      ...
    ]
  }
}
```



[Back to Main README](../../README.md)
