import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.keyboard.listener import KeyboardManager, check_accessibility_permissions
from src.audio.recorder import AudioRecorder
from src.transcription.transcriber import Transcriber
from src.llm.translate import Translator
from src.utils.logger import logger
import threading

def main():
    # 创建 Qt 应用
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 检查辅助功能权限
    check_accessibility_permissions()
    
    # 创建音频记录器和转录器
    audio_recorder = AudioRecorder()
    transcriber = Transcriber()
    translator = Translator()
    
    # 创建键盘管理器
    keyboard_manager = KeyboardManager(
        on_record_start=audio_recorder.start_recording,
        on_record_stop=lambda: transcriber.transcribe(audio_recorder.stop_recording()),
        on_translate_start=audio_recorder.start_recording,
        on_translate_stop=lambda: translator.translate(transcriber.transcribe(audio_recorder.stop_recording())[0]),
        on_reset_state=audio_recorder.reset
    )
    
    # 在新线程中启动键盘监听
    keyboard_thread = threading.Thread(target=keyboard_manager.start_listening, daemon=True)
    keyboard_thread.start()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 