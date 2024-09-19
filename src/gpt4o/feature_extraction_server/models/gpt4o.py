
from feature_extraction_server.core.model import Model
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.settings import FlagSetting, StringSetting
import cv2
from feature_extraction_server.core.dataformat import PngImage, OpencvImage

# def downsample_image_opencv(image, max_side_length=32):
    
#     # Get the original dimensions
#     height, width = image.shape[:2]
    
#     # Determine the scaling factor
#     if max(height, width) > max_side_length:
#         scaling_factor = max_side_length / float(max(height, width))
#     else:
#         scaling_factor = 1.0
    
#     # Calculate the new dimensions
#     new_dimensions = (int(width * scaling_factor), int(height * scaling_factor))
    
#     # Resize the image
#     return cv2.resize(image, new_dimensions, interpolation = cv2.INTER_AREA)

class Gpt4o(Model):
    
    consumer_type_name = "multi_thread_consumer"


    def _load_model(self):
        global HumanMessage, SystemMessage
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_openai import ChatOpenAI
        from langchain_core.utils.function_calling import convert_to_openai_function
        from langchain_community.tools import DuckDuckGoSearchResults

        self.tools = [DuckDuckGoSearchResults()]
        
        openai_key_setting = StringSetting("OPENAI_API_KEY", "", "The API key for OpenAI.")
        
        import os
        os.environ["OPENAI_API_KEY"] = openai_key_setting.get()

        self.model = ChatOpenAI(model="gpt-4o")
        self.model = self.model.bind_tools(self.tools)
        
        no_cuda_setting = FlagSetting("NO_CUDA", "If set, the model will not use CUDA.")
        self.no_cuda = no_cuda_setting.get()

    def chat_completion(self, user_message, system_message="You are a helpful assist that uses tools to enhance your responses with information from the internet.", user_image=None, config={}):
        
        # reduce image size
        THRESHOLD = 19 * 1024 * 1024
        if user_image is not None:
            estimated_file_size = len(user_image.to_png().to_binary())
            if estimated_file_size > THRESHOLD:
                scaling_factor = (THRESHOLD / estimated_file_size) ** 0.5
                cv2_image = user_image.to_opencv()
                new_width = int(cv2_image.shape[1] * scaling_factor)
                new_height = int(cv2_image.shape[0] * scaling_factor)
                resized_img = cv2.resize(cv2_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                user_image = OpencvImage.from_opencv(resized_img)
                
            
        
        messages = []
        
        if system_message is not None:
            messages.append(SystemMessage(content=system_message))
        
        content = [{"type":"text", "text":user_message}]
        if user_image is not None:
            content.append({"type":"image_url", "image_url": {"url":user_image.to_data_url()}})
        
        messages.append(HumanMessage(content))
        
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        prompt = ChatPromptTemplate.from_messages(

            messages + [ MessagesPlaceholder(variable_name="agent_scratchpad")]
        )
        
        from langchain.agents.format_scratchpad.openai_tools import (
            format_to_openai_tool_messages,
        )
        from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
        
        agent = (
            {
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | self.model
            | OpenAIToolsAgentOutputParser()
        )
        
        from langchain.agents import AgentExecutor
        
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        
        return {"assistant_message":agent_executor.invoke({})["output"]}
    
    def conditional_image_captioning(self, image, text, config={}):
        return {"caption":self.chat_completion(user_message=text, user_image=image, config=config)["assistant_message"]}