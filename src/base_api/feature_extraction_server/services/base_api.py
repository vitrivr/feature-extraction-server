
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

import threading as th

logger = logging.getLogger(__name__)



def wrap_output_model(output_model, batched) -> Type[BaseModel]:
    pyd = output_model.to_pydantic(False)
    
    # Dynamic name for the resulting class
    class_name = f"JobResponse{pyd.__name__}"
    
    if batched:
        class_name = f"Batched{class_name}"
        JobResponse = pydantic.create_model(
            class_name,
            status=(JobState, ...),  # Field with ellipsis for required fields
            result=(List[pyd], None),  # Optional field, defaulting to None
        )
    else:
        JobResponse = pydantic.create_model(
            class_name,
            status=(JobState, ...),  # Field with ellipsis for required fields
            result=(pyd, None),  # Optional field, defaulting to None
        )

    return JobResponse


class JobStatus(BaseModel):
    id: str
    status: JobState

# def wrap_function(func, args, input_model, output_model):
#     if not input_model is None:
#         async def wrapped_function(*, data : input_model = Body(...)) -> output_model:
#             return func(*args, dict(data))
#     else:
#         async def wrapped_function() -> output_model:
#             return func(*args)
#     return wrapped_function

def to_kebab_case(string):
    return string.replace("_", "-")

def to_snake_case(string):
    return string.replace("-", "_")

class ModelStatus(BaseModel):
    status: ModelState
    jobs: List[JobStatus]

class BaseApi(Service):
    
    @staticmethod
    def initialize_service(extraction_backend: ExtractionBackend, fast_api_app: FastApiApp):
        baseapi = BaseApi(extraction_backend=extraction_backend)
        baseapi.add_routes(fast_api_app.app)
        return baseapi
    
    def __init__(self, extraction_backend):
        self._extraction_backend = extraction_backend
        self._active_jobs = {}
    
    def add_routes(self, app):
        app.add_api_route('/api/tasks', self.list_all_tasks, methods=['GET'], name="list-all-tasks", tags=["tasks"])
        app.add_api_route('/api/tasks/{task}/models', self.list_all_models_for_task, methods=['GET'], name="list-all-models-for-task", tags=["tasks"])
        
        app.add_api_route('/api/models', self.list_all_models, methods=['GET'], name="list_all_models", tags=["models"])
        app.add_api_route('/api/models/{model}/tasks', self.list_all_tasks_for_model, methods=['GET'], name="list-all-tasks-for-model", tags=["models"])
        app.add_api_route('/api/models/{model}/start', self.start_model, methods=['POST'], name="start-model", tags=["models"])
        app.add_api_route('/api/models/{model}/stop', self.stop_model, methods=['POST'], name="stop-model", tags=["models"])
        app.add_api_route('/api/models/{model}/status', self.get_model_status, methods=['GET'], name="get-model-status", tags=["models"])
        
        
            
        for task in self._extraction_backend.iterate_tasks():
            tn = to_kebab_case(task.name)
            app.add_api_route(f'/api/tasks/{tn}/' + '{model}/jobs', self.make_new_job(task, batched=False), methods=['POST'], name=f"new-job", tags=[tn])
            app.add_api_route(f'/api/tasks/{tn}/jobs/' + '{job}', self.make_features(task, batched=False), methods=['GET'], name=f"get-job-results", tags=[tn])
            app.add_api_route(f'/api/tasks/{tn}/batched/' + '{model}/jobs', self.make_new_job(task, batched=True), methods=['POST'], name=f"new-batched-job", tags=[tn])
            app.add_api_route(f'/api/tasks/{tn}/batched/jobs/' + '{job}', self.make_features(task, batched=True), methods=['GET'], name=f"get-batched-job-results", tags=[tn])
            
    
    def make_features(self, task, batched):
        wrapped_output_model = wrap_output_model(task.get_output_data_model(), batched)
        async def features(job:str) -> wrapped_output_model:
            try:
                out = self._features(job_id=job)
                if "result" in out and batched:
                    out["result"] = list(task.get_output_data_model().unroll(out["result"]))
                return out
            except Exception as e:
                logger.error(f"Error while fetching job {job}: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while fetching job: {e}") from e
        return features
    
    def _features(self, job_id):
        job = self._active_jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        state = job.get_state()
        if state == JobState.failed:
            job.reraise_exception()
        if state == JobState.complete:
            self._active_jobs.pop(job_id)
            result = job.get_result()
            return jsonable_encoder({"status": state, "result": result})
        else:
            return jsonable_encoder({"status": state})
        
    
    def make_new_job(self, task, batched):
        input_model = task.get_input_data_model().to_pydantic(batched)
        async def features(model:str, data : input_model = Body(...)) -> JobStatus:
            try:
                model = self._extraction_backend.get_model(model_name = to_snake_case(model))
                return self._new_job(task, model, dict(data), batched)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while creating job: {e}") from e
        return features
    
    def _new_job(self, task, model, json_data, batched):
        try:
            model.start()
        except ModelAlreadyStartedException:
            pass
        
        job = self._extraction_backend.create_job(model_name=to_snake_case(model.name), task_name=to_snake_case(task.name), kwargs=json_data,batched=batched)
        self._active_jobs[job.id] = job
        job.start()
        return {"id": job.id, "status":job.get_state()}


    async def list_all_tasks(self) -> list[str]:
        task_names = []
        for task in self._extraction_backend.iterate_tasks():
            task_names.append(to_kebab_case(task.name))
        return task_names

    async def list_all_models(self) -> list[str]:
        model_names = []
        for model in self._extraction_backend.iterate_models():
            model_names.append(to_kebab_case(model.name))
        return model_names

    async def list_all_tasks_for_model(self, model:str) -> list[str]:
        task_names = []
        app_model = self._extraction_backend.get_model(model_name = to_snake_case(model))
        for task in app_model.iterate_tasks():
            task_names.append(to_kebab_case(task.name))
        return task_names

    async def list_all_models_for_task(self, task:str) -> list[str]:
        model_names = []
        app_task = self._extraction_backend.get_task(to_snake_case(task))
        for model in app_task.iterate_models():
            model_names.append(to_kebab_case(model.name))
        return model_names

    async def start_model(self, model:str):
        self._extraction_backend.get_model(model_name=to_snake_case(model)).start()
        return Response(status_code=HTTP_200_OK)

    async def stop_model(self, model:str):
        self._extraction_backend.get_model(model_name = to_snake_case(model)).stop()
        return Response(status_code=HTTP_200_OK)
    
    async def get_model_status(self, model:str) -> ModelStatus:
        job_statuses = []
        model = self._extraction_backend.get_model(model_name=to_snake_case(model))
        for job in model.get_jobs():
            job_statuses.append({"id":job.id, "status":job.get_state()})
        return {"status":model.get_state(),
                "jobs":job_statuses}
