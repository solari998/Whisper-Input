import os
from ..transcription.whisper import WhisperProcessor
from ..transcription.senseVoiceSmall import SenseVoiceSmallProcessor

class Translator:
    def __init__(self):
        self._whisper = WhisperProcessor()
        self._sense_voice = SenseVoiceSmallProcessor()
    
    def translate(self, text):
        """将文本翻译为英文
        
        Args:
            text: 要翻译的文本
            
        Returns:
            tuple: (翻译后的文本, 错误信息)
        """
        if not text:
            return None, "没有需要翻译的文本"
            
        # 根据配置选择服务
        service = os.getenv("SERVICE_PLATFORM", "siliconflow").lower()
        
        if service == "groq":
            processor = self._whisper
        elif service == "siliconflow":
            processor = self._sense_voice
        else:
            return None, f"无效的服务平台: {service}"
            
        # 调用翻译模式
        return processor.process_audio(text, mode="translations", prompt="")