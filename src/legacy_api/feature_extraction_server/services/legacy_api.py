
from feature_extraction_server.services.extraction_backend import ExtractionBackend
from feature_extraction_server.services.fast_api_app import FastApiApp
from feature_extraction_server.core.exceptions import ModelAlreadyStartedException
from feature_extraction_server.core.execution_state import JobState, ModelState
import logging
from fastapi import Body
from simple_plugin_manager.service import Service
import time
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Type, List
from fastapi.encoders import jsonable_encoder
import pydantic

from starlette.responses import Response
from starlette.status import HTTP_200_OK

logger = logging.getLogger(__name__)



def to_kebab_case(string):
    return string.replace("_", "-")

def to_snake_case(string):
    return string.replace("-", "_")



class LegacyApi(Service):
    
    @staticmethod
    def initialize_service(extraction_backend: ExtractionBackend, fast_api_app: FastApiApp):
        baseapi = LegacyApi(extraction_backend=extraction_backend)
        baseapi.add_routes(fast_api_app.app)
        return baseapi
    
    def __init__(self, extraction_backend):
        self._extraction_backend = extraction_backend
    
    def add_routes(self, app):
            
        for task in self._extraction_backend.iterate_tasks():
            tn = to_kebab_case(task.name)
            app.add_api_route(f'/api/legacy/tasks/{tn}/' + '{model}/jobs', self.make_new_job_results(task), methods=['POST'], name=f"new-job-results", tags=[tn])
        
    
    def make_new_job_results(self, task):
        input_model = task.get_input_data_model().to_pydantic(batched=False)
        output_model = task.get_output_data_model().to_pydantic(batched=False)
        async def features(model:str, data : input_model = Body(...)) -> output_model:
            try:
                model = self._extraction_backend.get_model(model_name = to_snake_case(model))
                try:
                    model.start()
                except ModelAlreadyStartedException:
                    pass
                
                job = self._extraction_backend.create_job(model_name=to_snake_case(model.name), task_name=to_snake_case(task.name), kwargs=dict(data),batched=False)
                job.start()
                job.block()
                state = job.get_state()
                if state == JobState.failed:
                    job.reraise_exception()
                if state == JobState.complete:
                    return jsonable_encoder(job.get_result())
                else:
                    raise Exception(f"Job is in state {state}")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while executing job: {e}") from e
        return features