from pydantic import create_model
from feature_extraction_server.core.dataformat import IDataType
from typing import List, get_origin


class Field:
    def __init__(self, name, batched, type, optional):
        self.name = name
        self.batched = batched
        self.type = type
        self.optional = optional

class DataModel:
    def __init__(self, name, *fields: list[Field]):
        self.name = name
        self.fields = fields
    
    def to_pydantic(self, batched):
        field_definitions = {}
        for field in self.fields:
            
            tt = str if isinstance(field.type, type) and issubclass(field.type, IDataType) else field.type
            
            if batched and field.batched:
                final_type = List[tt]
            else:
                final_type = tt
            
            # Set default values based on whether the field is optional
            if field.optional:
                field_definitions[field.name] = (final_type, None)
            else:
                field_definitions[field.name] = (final_type, ...)

        # Set the class name depending on whether it's batched or not
        name = f"Batched{self.name}" if batched else self.name

        # Create the Pydantic model dynamically using the prepared field definitions
        data_model_class = create_model(name, **field_definitions)
        return data_model_class
    
    def preprocess(self, data: dict, batched: bool):
        output_data = {}
        for field in self.fields:
            if field.optional and data.get(field.name) is None:
                continue
            if isinstance(field.type, type) and issubclass(field.type, IDataType):
                if field.batched and batched:
                    output_data[field.name] = [field.type.from_data_url(d) for d in data[field.name]]
                else:
                    output_data[field.name] = field.type.from_data_url(data[field.name])
            else:
                output_data[field.name] = data[field.name]
        return output_data
    
    def postprocess(self, data: dict, batched: bool):
        output_data = {}
        for field in self.fields:
            if field.optional and field.name not in data:
                continue
            if isinstance(field.type, type) and issubclass(field.type, IDataType):
                if field.batched and batched:
                    output_data[field.name] = [field.type.to_data_url(d) for d in data[field.name]]
                else:
                    output_data[field.name] = field.type.to_data_url(data[field.name])
            else:
                output_data[field.name] = data[field.name]
        return output_data
    
    def unroll(self, data: dict):
        maxlen = max([len(data[field.name]) for field in self.fields if field.batched])
        
        for i in range(maxlen):
            datapoint = {}
            for field in self.fields:
                if field.optional and field.name not in data:
                    continue
                if field.batched:
                    datapoint[field.name] = data[field.name][i%len(data[field.name])]
                else:
                    datapoint[field.name] = data[field.name]
        
            yield datapoint
    
    def roll(self, data: list[dict]):
        output_data = {}
        for field in self.fields:
            if field.batched:
                output_data[field.name] = []
        
        for datapoint in data:
            for field in self.fields:
                if field.optional and field.name not in datapoint:
                    continue
                if field.batched:
                    output_data[field.name].append(datapoint[field.name])
                else:
                    output_data[field.name] = datapoint[field.name]
        
        return output_data
    
    
    def expand_to_batched(self, data):
        output = {}
        for field in self.fields:
            if field.batched:
                output[field.name] = [data[field.name]]
            else:
                output[field.name] = data[field.name]
        return output
    
    def squeeze(self, data):
        output = {}
        for field in self.fields:
            if field.batched:
                output[field.name] = data[field.name][0]
            else:
                output[field.name] = data[field.name]
        return output