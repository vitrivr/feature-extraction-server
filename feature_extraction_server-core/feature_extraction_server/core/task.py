import logging
from simple_plugin_manager.utils import convert_to_snake_case
from feature_extraction_server.core.datamodel import DataModel
from feature_extraction_server.core.exceptions import MissingTaskImplementationException

logger = logging.getLogger(__name__)

class Task:
    
    input : DataModel
    output : DataModel
    
    def __init__(self):
        self.name = self.get_name()
    
    @classmethod
    def get_name(cls):
        type_name = cls.__name__
        return convert_to_snake_case(type_name)
    
    @classmethod
    def wrap_model(cls, model, batched):
        def single_to_single(data):
            if data["config"] is None:
                data["config"] = {}
            input_datamodel = cls.get_input_data_model()
            output_datamodel = cls.get_output_data_model()
            preprocessed_data = input_datamodel.preprocess(data, False)
            result = model.get_task_implementation(cls.name)(**preprocessed_data)
            return output_datamodel.postprocess(result, False)
        
        def batched_to_single(data):
            if data["config"] is None:
                data["config"] = {}
            input_datamodel = cls.get_input_data_model()
            output_datamodel = cls.get_output_data_model()
            preprocessed_data = input_datamodel.preprocess(data, True)
            result = []
            for datapoint in input_datamodel.unroll(preprocessed_data):
                result.append(model.get_task_implementation(cls.get_name())(**datapoint))
            result = output_datamodel.roll(result)
            return output_datamodel.postprocess(result, True)
        
        def single_to_batched(data):
            if data["config"] is None:
                data["config"] = {}
            input_datamodel = cls.get_input_data_model()
            output_datamodel = cls.get_output_data_model()
            preprocessed_data = input_datamodel.expand_to_batched(input_datamodel.preprocess(data, False))
            result = model.get_task_implementation(f"batched_{cls.get_name()}")(**preprocessed_data)
            return output_datamodel.postprocess(output_datamodel.squeeze(result), False)
        
        def batched_to_batched(data):
            if data["config"] is None:
                data["config"] = {}
            datamodel = cls.get_input_data_model()
            output_datamodel = cls.get_output_data_model()
            preprocessed_data = datamodel.preprocess(data, True)
            result = model.get_task_implementation(f"batched_{cls.get_name()}")(**preprocessed_data)
            return output_datamodel.postprocess(result, True)
        
        single_implemented = False
        batched_implemented = False
        
        try:
            model.get_task_implementation(cls.get_name())
            single_implemented = True
        except MissingTaskImplementationException:
            single_implemented = False
        
        try:
            model.get_task_implementation(f"batched_{cls.get_name()}")
            batched_implemented = True
        except MissingTaskImplementationException:
            batched_implemented = False
        
        if batched:
            if batched_implemented:
                return batched_to_batched
            elif single_implemented:
                return batched_to_single
        else:
            if single_implemented:
                return single_to_single
            elif batched_implemented:
                return single_to_batched
        
        raise MissingTaskImplementationException(f"Task {cls.get_name()} is not implemented")
        
    @classmethod
    def get_input_data_model(self):
        return self.input
    
    @classmethod
    def get_output_data_model(self):
        return self.output
    
    def setup(self):
        pass
    
    @classmethod
    def is_implemented(cls, model):
        try:
            model.get_task_implementation(cls.get_name())
            return True
        except MissingTaskImplementationException:
            ...
        
        try:
            model.get_task_implementation(f"batched_{cls.get_name()}")
            return True
        except MissingTaskImplementationException:
            ...
        
        return False

