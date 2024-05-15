# Conditional Image Captioning
This plugin adds the conditional image captioning task (batched and non-batched) which allows you to generate text from image data and a prompt.

## Installation

This plugin requires core and simple_plugin_manager as dependencies. For source, local and containerized installation instructions please see the main [README](../../README.md).

To execute the task, a plugin which includes a model that supports the conditional image captioning task should be installed. 

Currently, the following models support conditional image captioning:
- [blip](../blip/README.md)
- [blip2](../blip2/README.md)

To expose the task as an endpoint the [fastapi](../fastapi/README.md) plugin and one of the following apis should be installed:
- [base_api](../base_api/README.md)
- [legacy_api](../legacy_api/README.md)

## Usage

As input this task requires the following fields:

| Key | Required | Batched | Type| Description |
| --- | --- | --- | --- | --- |
| `image` | Yes | Yes | image data | The image that needs captioning |
| `text` | Yes | Yes | string | A specified prefix for the caption that should be generated. For example `"Question: What is depicted in this photograph? Answer:"` |
| `config` | No | Yes | dict | Any additional arguments (see the model documentation) |


As ouput this task returns the following fields:

| Key | Batched | Type| Description |
| --- | --- | --- | --- |
| `caption` | Yes | string | The generated caption |

When the task is executed in batched mode, the batched fields are given (or returned) as lists, whereas the non-batched fields are given as simple values.


### Example

For the `/api/tasks/conditional-image-captioning/{model}/jobs` endpoint defined in [base_api](../base_api/README.md) the following request body serves as an example:

```json
{
  "image": "data:image/jpeg;base64,UklGRhDUCwB...",
  "text": "Question: What is depicted in this photograph? Answer:",
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

Later, the result can be retrieved using `/api/tasks/conditional-image-captioning/jobs/05032039-e7dd-4ca5-8941-ebff9f5f2e09`:

```json
{
  "status": "complete",
  "result": {
    "caption": "A cat"
  }
}
```


[Back to Main README](../../README.md)
