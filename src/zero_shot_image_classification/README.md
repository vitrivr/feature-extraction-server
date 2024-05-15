# Zero Shot Image Classification

This plugin adds the zero shot image classification task (batched and non-batched) which allows you to probabalistically classify images into classes that the model may or may not have seen before.

## Installation

This plugin requires core and simple_plugin_manager as dependencies. For source, local and containerized installation instructions please see the main [README](../../README.md).

To execute the task, a plugin which includes a model that supports the zero shot image classification task should be installed. 

Currently, the following models support zero shot image classification:
- [CLIP ViT Large Patch 14](../clip_vit_large_patch14/README.md)
- [Open CLIP ViT B32](../open_clip_vit_b32/README.md)

To expose the task as an endpoint the [fastapi](../fastapi/README.md) plugin and one of the following apis should be installed:
- [base_api](../base_api/README.md)
- [legacy_api](../legacy_api/README.md)

## Usage

As input this task requires the following fields:

| Key | Required | Batched | Type| Description |
| --- | --- | --- | --- | --- |
| `image` | Yes | Yes | image data | The image that needs to classified |
| `classes` | Yes | No | list of strings | A list of strings that represents the catalogue of classes |
| `config` | No | Yes | dict | Any additional arguments (see the model documentation) |


As ouput this task returns the following fields:

| Key | Batched | Type| Description |
| --- | --- | --- | --- |
| `probabilities` | Yes | list of floats | list of floating point numbers between 0 and 1 that represent the probability that the image belongs to a class |

When the task is executed in batched mode, the batched fields are given (or returned) as lists, whereas the non-batched fields are given as simple values.


### Example

For the `/api/tasks/zero-shot-image-classification/{model}/jobs` endpoint defined in [base_api](../base_api/README.md) the following request body serves as an example:

```json
{
  "image": "data:image/jpeg;base64,UklGRhDUCwB...",
  "classes": [
    "cat",
    "dog"
  ],
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

Later, the result can be retrieved using `/api/tasks/zero-shot-image-classification/jobs/05032039-e7dd-4ca5-8941-ebff9f5f2e09`:

```json
{
  "status": "complete",
  "result": {
    "probabilities": [
      0.8,
      0.2
    ]
  }
}
```


[Back to Main README](../../README.md)

