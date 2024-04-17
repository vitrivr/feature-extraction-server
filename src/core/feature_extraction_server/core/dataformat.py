import io
from typing import Tuple
import base64
import numpy as np    
import re
import soundfile as sf
import pydub

def process_dataurl(dataurl):
    """
    Process a dataurl and extract media type, encoding, and data.
    
    Args:
    - dataurl (str): The dataurl string to process.
    
    Returns:
    - dict: A dictionary containing the media type, encoding, and data.
    """
    
    # Regular expression to match dataurl format
    pattern = r'data:(?P<mediatype>.*?)(;(?P<encoding>base64))?,(?P<data>.*)'
    match = re.match(pattern, dataurl)
    
    if not match:
        raise ValueError("Invalid data URL format")
    
    return {
        "mediatype": match.group("mediatype") or None,
        "encoding": match.group("encoding") or None,
        "data": match.group("data")
    }

import abc 

class IDataType(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def from_data_url(data_url:str):
        pass
    
    @abc.abstractmethod
    def to_data_url(self):
        pass

class IRawData(IDataType):
    def to_format(self, format):
        if format is BinaryData:
            return self.to_binary()
        if format is Base64Data:
            return self.to_base64()
        if format is BinaryStreamData:
            return self.to_binary_stream()
        
    
    @staticmethod
    def from_data_url(data_url:str):
        raise NotImplementedError
    
    def to_data_url(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def to_binary(self) -> bytes:
        pass
    
    @abc.abstractmethod
    def to_base64(self) -> str:
        pass
    
    @abc.abstractmethod
    def to_binary_stream(self) -> io.BytesIO:
        pass
    
    @classmethod
    def from_binary(cls, data: bytes):
        pass

    @classmethod
    def from_base64(cls, data: str):
        pass
    
    @classmethod
    def from_binary_stream(cls, data: io.BytesIO):
        pass

class BinaryData(IRawData):
    def __init__(self, data: bytes):
        self._data = data
    
    def to_binary(self) -> bytes:
        return self._data
    
    def to_base64(self) -> str:
        return base64.b64encode(self._data).decode('utf-8')
    
    def to_binary_stream(self) -> io.BytesIO:
        return io.BytesIO(self._data)
    
    @classmethod
    def from_binary(cls, data: bytes):
        return cls(data)

    @classmethod
    def from_base64(cls, data: str):
        return cls(Base64Data(data).to_binary())
    
    @classmethod
    def from_binary_stream(cls, data: io.BytesIO):
        return cls(BinaryData(data).to_binary())

class Base64Data(IRawData):
    def __init__(self, data: str):
        self._data = data
    
    def to_binary(self) -> bytes:
        return base64.b64decode(self._data)
      
    def to_base64(self) -> str:
        return self._data
    
    def to_binary_stream(self) -> io.BytesIO:
        return io.BytesIO(base64.b64decode(self._data))

    @classmethod
    def from_binary(cls, data: bytes):
        return cls(BinaryData(data).to_base64())

    @classmethod
    def from_base64(cls, data: str):
        return cls(data)
    
    @classmethod
    def from_binary_stream(cls, data: io.BytesIO):
        return cls(BinaryStreamData(data).to_base64())

class BinaryStreamData(IRawData):
    def __init__(self, data: io.BytesIO):
        self._data = data
    
    def to_binary(self) -> bytes:
        return self._data.getvalue()
    
    def to_base64(self) -> str:
        return base64.b64encode(self._data.getvalue()).decode('utf-8')
    
    def to_binary_stream(self) -> io.BytesIO:
        return self._data
    
    @classmethod
    def from_binary(cls, data: bytes):
        return cls(BinaryData(data).to_binary_stream())
    
    @classmethod
    def from_base64(cls, data: str):
        return cls(Base64Data(data).to_binary_stream())
    
    @classmethod
    def from_binary_stream(cls, data: io.BytesIO):
        return cls(data)


class IAudioFormat(IDataType):
    
    def to(self, format: type):
        if format is WavAudio:
            return self.to_wav()
        if format is NumpyAudio:
            return self.to_numpy()
        if format is PyDubAudio:
            return self.to_pydub()
        raise ValueError("Invalid audio format")
    
    @staticmethod
    def from_data_url(data_url: str):
        # first process the dataurl
        url_dict = process_dataurl(data_url)
        
        # process the data with the encoding
        if url_dict["encoding"] == "base64":
            data = Base64Data(url_dict["data"])
        elif url_dict["encoding"] is None:
            data = BinaryData(url_dict["data"])
        else:
            raise ValueError("Invalid data URL encoding")
        
        # wrap the data in the appropriate audio format
        if url_dict["mediatype"] == "audio/wav":
            return WavAudio(data)
        raise ValueError("Invalid data URL media type")
    
    def to_data_url(self)->str:
        self.to_wav().to_data_url()
    
    def to_wav(self)-> IRawData:
        pass
    
    def to_numpy(self)-> Tuple[np.ndarray, int]:
        pass
    
    def to_pydub(self):
        pass
        
    
    @classmethod
    def from_wav(cls, data: IRawData):
        return cls(WavAudio(data).to(cls))
    
    @classmethod
    def from_numpy(cls, data: Tuple[np.ndarray, int]):
        return cls(NumpyAudio(data).to(cls))
    
    @classmethod
    def from_pydub(cls, data: pydub.AudioSegment):
        return cls(PyDubAudio(data).to(cls))
    
class NumpyAudio(IAudioFormat):
    def __init__(self, data: Tuple[np.ndarray, int]):
        self.samples = data[0]
        self.sample_rate = data[1]
    
    def to_wav(self)-> IRawData:
        byte_stream = io.BytesIO()
        sf.write(byte_stream, self.samples, self.sample_rate)
        return BinaryStreamData(byte_stream)
    
    def to_numpy(self)-> Tuple[np.ndarray, int]:
        return self.samples, self.sample_rate
    
    def to_pydub(self):
        return pydub.AudioSegment(data=self.samples.tobytes(), sample_width=self.samples.dtype.itemsize, frame_rate=self.sample_rate, channels=self.samples.shape[1])
    
    def resample(self, sample_rate: int):
        pydub_audio = PyDubAudio(self.to_pydub())
        return pydub_audio.resample(sample_rate)
        
    
class WavAudio(IAudioFormat):
    def __init__(self, data: IRawData):
        self._data = data
    
    def to_wav(self)-> IRawData:
        return self._data
    
    def to_data_url(self) -> str:
        base64_data = self._data.to_base64()
        return f"data:audio/wav;base64,{base64_data}"
    
    def to_numpy(self)-> Tuple[np.ndarray, int]:
        byte_stream = self._data.to_binary_stream()
        samples, sample_rate = sf.read(byte_stream)
        return samples, sample_rate
    
    def to_pydub(self):
        return pydub.AudioSegment.from_wav(self._data.to_binary_stream())
    
    def resample(self, sample_rate: int):
        pydub_audio = PyDubAudio(self.to_pydub())
        return pydub_audio.resample(sample_rate)

class PyDubAudio(IAudioFormat):
    def __init__(self, data: pydub.AudioSegment):
        self._data = data
    
    def to_wav(self)-> IRawData:
        byte_stream = io.BytesIO()
        self._data.export(byte_stream, format='wav')
        return BinaryStreamData(byte_stream)
    
    def to_numpy(self)-> Tuple[np.ndarray, int]:
        samples = np.frombuffer(self._data.raw_data, np.int16)
        return samples, self._data.frame_rate
    
    def to_pydub(self):
        return self._data
    
    def resample(self, sample_rate: int):
        _data = self._data.set_frame_rate(sample_rate)
        return PyDubAudio(_data)

import cv2, PIL.Image
import abc


class IImageFormat(IDataType):
    
    def to(self, format: type):
        if format is PngImage:
            return self.to_png()
        if format is JpegImage:
            return self.to_jpeg()
        if format is NumpyImage:
            return self.to_numpy()
        if format is PillowImage:
            return self.to_pillow()
        if format is OpencvImage:
            return self.to_opencv()
        raise ValueError("Invalid image format")
    
    @staticmethod
    def from_data_url(data_url: str):
        try:
            url_dict = process_dataurl(data_url)
        except ValueError:
            # if the dataurl is invalid, try to parse it as a base64 string
            data = Base64Data(data_url)
            return IImageFormat.from_unknown(data)
        
        if url_dict["encoding"] == "base64":
            data = Base64Data(url_dict["data"])
        elif url_dict["encoding"] is None:
            data = BinaryData(url_dict["data"])
        else:
            raise ValueError("Invalid data URL encoding")
        
        # wrap the data in the appropriate image format
        if url_dict["mediatype"] == "image/png":
            return PngImage(data)
        if url_dict["mediatype"] == "image/jpeg":
            return JpegImage(data)
        if url_dict["mediatype"] == "image/jpg":
            return JpegImage(data)
        raise ValueError("Invalid data URL media type")
    
    def to_data_url(self)->str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def to_png(self)-> IRawData:
        pass
    
    @abc.abstractmethod
    def to_jpeg(self)-> IRawData:
        pass
    
    @abc.abstractmethod
    def to_numpy(self)-> np.ndarray:
        pass
    
    @abc.abstractmethod
    def to_pillow(self)-> PIL.Image:
        pass
    
    @abc.abstractmethod
    def to_opencv(self)-> np.ndarray:
        pass
    
    @classmethod
    def from_jpeg(cls, data: IRawData):
        return cls(JpegImage(data).to(cls))
    
    @classmethod
    def from_png(cls, data: IRawData):
        return cls(PngImage(data).to(cls))
    
    @classmethod
    def from_numpy(cls, data: np.ndarray):
        return cls(NumpyImage(data).to(cls))
    
    @classmethod
    def from_pillow(cls, data: PIL.Image):
        return cls(PillowImage(data).to(cls))
    
    @classmethod
    def from_opencv(cls, data: np.ndarray):
        return cls(OpencvImage(data).to(cls))
    
    @staticmethod
    def from_unknown(data: IRawData):
        img = PIL.Image.open(data.to_binary_stream())
        if img.format == "PNG":
            return PngImage(data)
        if img.format == "JPEG":
            return JpegImage(data)
        else:
            raise ValueError("Unknown image format")

class PillowImage(IImageFormat):
    def __init__(self, data: PIL.Image):
        self._data = data
    
    def to_png(self)-> IRawData:
        byte_stream = io.BytesIO()
        self._data.save(byte_stream, format='PNG')
        return BinaryStreamData(byte_stream)
    
    def to_jpeg(self)-> IRawData:
        byte_stream = io.BytesIO()
        self._data.save(byte_stream, format='JPEG')
        return BinaryStreamData(byte_stream)
    
    def to_numpy(self)-> np.ndarray:
        return np.array(self._data)
    
    def to_opencv(self) -> np.ndarray:
        # Convert RGB to BGR
        return cv2.cvtColor(np.array(self._data), cv2.COLOR_RGB2BGR)

class PngImage(IImageFormat):
    
    def __init__(self, data: IRawData):
        self._data = data
        
    def to_png(self)-> IRawData:
        return self._data
    
    def to_jpeg(self)-> IRawData:
        byte_stream = io.BytesIO()
        img = PIL.Image.open(self._data.to_binary_stream())
        img.save(byte_stream, format='JPEG')
        return BinaryStreamData(byte_stream)
    
    def to_numpy(self)-> np.ndarray:
        img = PIL.Image.open(self._data.to_binary_stream())
        return np.array(img)
    
    def to_pillow(self)-> PIL.Image:
        return PIL.Image.open(self._data.to_binary_stream())
    
    def to_opencv(self) -> np.ndarray:
        # Convert RGB to BGR
        return cv2.cvtColor(np.array(self.to_pillow()), cv2.COLOR_RGB2BGR)
    
class JpegImage(IImageFormat):
    
    def __init__(self, data: IRawData):
        self._data = data
        
    def to_png(self)-> IRawData:
        byte_stream = io.BytesIO()
        img = PIL.Image.open(self._data.to_binary_stream())
        img.save(byte_stream, format='PNG')
        return BinaryStreamData(byte_stream)
    
    def to_jpeg(self)-> IRawData:
        return self._data
    
    def to_numpy(self)-> np.ndarray:
        img = PIL.Image.open(self._data.to_binary_stream())
        return np.array(img)
    
    def to_pillow(self)-> PIL.Image:
        return PIL.Image.open(self._data.to_binary_stream())
    
    def to_opencv(self) -> np.ndarray:
        # Convert RGB to BGR
        return cv2.cvtColor(np.array(self.to_pillow()), cv2.COLOR_RGB2BGR)

class NumpyImage(IImageFormat):
    
    def __init__(self, data: np.ndarray):
        self._data = data
        
    def to_png(self)-> IRawData:
        byte_stream = io.BytesIO()
        img = PIL.Image.fromarray(self._data)
        img.save(byte_stream, format='PNG')
        return BinaryStreamData(byte_stream)
    
    def to_jpeg(self)-> IRawData:
        byte_stream = io.BytesIO()
        img = PIL.Image.fromarray(self._data)
        img.save(byte_stream, format='JPEG')
        return BinaryStreamData(byte_stream)
    
    def to_numpy(self)-> np.ndarray:
        return self._data
    
    def to_pillow(self)-> PIL.Image:
        return PIL.Image.fromarray(self._data)
    
    def to_opencv(self) -> np.ndarray:
        # Convert RGB to BGR
        return cv2.cvtColor(self._data, cv2.COLOR_RGB2BGR)

class OpencvImage(IImageFormat):
    
    def __init__(self, data: np.ndarray):
        self._data = data
    
    def to_png(self)-> IRawData:
        byte_stream = io.BytesIO()
        img = PIL.Image.fromarray(cv2.cvtColor(self._data, cv2.COLOR_BGR2RGB))
        img.save(byte_stream, format='PNG')
        return BinaryStreamData(byte_stream)
    
    def to_jpeg(self)-> IRawData:
        byte_stream = io.BytesIO()
        img = PIL.Image.fromarray(cv2.cvtColor(self._data, cv2.COLOR_BGR2RGB))
        img.save(byte_stream, format='JPEG')
        return BinaryStreamData(byte_stream)
    
    def to_numpy(self) -> np.ndarray:
        # Convert BGR to RGB
        return cv2.cvtColor(self._data, cv2.COLOR_BGR2RGB)
    
    def to_pillow(self)-> PIL.Image:
        # Convert BGR to RGB
        return PIL.Image.fromarray(cv2.cvtColor(self._data, cv2.COLOR_BGR2RGB))
    
    def to_opencv(self) -> np.ndarray:
        return self._data