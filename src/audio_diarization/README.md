# Audio Diarization

This plugin adds the audio diarization task (batched and non-batched).

NOTE: this plugin is not ready

## Installation
This plugin requires core and simple_plugin_manager as dependencies. For source, local and containerized installation instructions please see the main [README](../../README.md).

To execute the task, a plugin which includes a model that supports the audio diarization task should be installed. 

Currently, the following models support audio diarization:
- [pyannote](../pyannote/README.md)

To expose the task as an endpoint the [fast_api](../base_api/README.md) plugin and one of the following apis should be installed:
- [base_api](../base_api/README.md)
- [legacy_api](../legacy_api/README.md)

## Usage
TODO

[Back to Main README](../../README.md)
