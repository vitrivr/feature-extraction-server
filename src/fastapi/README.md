# Fast API Plugin

This plugin adds a REST server using FastAPI. By default, no endpoints are included but it can be extended.


## Extensions

These plugins add endpoints to this server.

- [This](src/base_api/README.md) plugin extends the server with endpoints that allow the user to create new jobs and get results.
- [This](src/legacy_api/README.md) plugin defines simpler endpoints that allow the user to both create new jobs and get results in a single 


## Configuration

Installing this plugin adds the following settings:

| Name                  | Command Line Argument   | Description                                                                     |
|-----------------------|-------------------------|---------------------------------------------------------------------------------|
| SPEC_ROUTE            | --spec-route            | The route at which the openapi spec is generated.                               |
| HOST                  | --host                  | The host to bind to.                                                            |
| PORT                  | --port                  | The port to bind to.                                                            |

[Back to Main README](../../README.md)