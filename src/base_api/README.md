# Base API

This plugin extends the server with endpoints that allow the user to create new jobs and get results. It uses the installed tasks to generate batched and non-batched endpoints.

For more information you can check out the swagger ui under `/docs`.

## Endpoints

For image and audio data, this endpoint expects a base 64 data url (for example jpeg or wav).

### Create New Job

Use this endpoint to create a new job with your input data.

POST `/api/tasks/{task}/{model}/jobs`

### Get Job Results

Use this endpoint to retrieve the result based on your job id.

GET `/api/tasks/{task}/jobs/{job}`

### Create Batched Job

Use this endpoint to create a new batched job with your input data.

POST `/api/tasks/{task}/batched/{model}/jobs`

### Get Job Results

Use this endpoint to retrieve the batched result based on your job id. The result will be a list of mappings.

GET `/api/tasks/{task}/batched/jobs/{job}`

[Back to Main README](../../README.md)