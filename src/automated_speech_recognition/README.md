# Automated Speech Recognition
This plugin adds the automated speech recognition task (batched and non-batched) which allows you to generate text from speech in the form of audio data.

## Installation

This plugin requires core and simple_plugin_manager as dependencies. For source, local and containerized installation instructions please see the main [README](../../README.md).

To execute the task, a plugin which includes a model that supports the automated speech recognition task should be installed. 

Currently, the following models support automated speech recognition:
- [whisper](../whisper/README.md)

To expose the task as an endpoint the [fastapi](../fastapi/README.md) plugin and one of the following apis should be installed:
- [base_api](../base_api/README.md)
- [legacy_api](../legacy_api/README.md)

## Usage

As input this task requires the following fields:

| Key | Required | Batched | Type| Description |
| --- | --- | --- | --- | --- |
| `audio` | Yes | Yes | audio data | The audio from which the speech needs to be generated |
| `config` | No | Yes | dict | Any additional arguments (see the model documentation) |


As ouput this task returns the following fields:

| Key | Batched | Type| Description |
| --- | --- | --- | --- |
| `transcript` | Yes | string | The generated text |

When the task is executed in batched mode, the batched fields are given (or returned) as lists, whereas the non-batched fields are given as simple values.

### Example

For the `/api/tasks/automated-speech-recognition/{model}/jobs` endpoint defined in [base_api](../base_api/README.md) the following request body serves as an example:

```json
{
  "audio": "data:audio/wav;base64,UklGRhDUCwB...",
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

Later, the result can be retrieved using `/api/tasks/automated-speech-recognition/jobs/05032039-e7dd-4ca5-8941-ebff9f5f2e09`:

```json
{
  "status": "complete",
  "result": {
    "transcript": "Hello"
  }
}
```



[Back to Main README](../../README.md)
