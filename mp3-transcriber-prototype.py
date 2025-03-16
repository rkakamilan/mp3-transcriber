import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QFileDialog, QListWidget, QProgressBar, QLabel, 
                             QTextEdit, QComboBox, QGroupBox, QGridLayout, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# 将来的にWhisperを使用する部分のプレースホルダー
class TranscriptionThread(QThread):
    """音声文字起こし処理を行うスレッド"""
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, str)  # ファイル名、テキスト内容

    def __init__(self, file_path, language='ja'):
        super().__init__()
        self.file_path = file_path
        self.language = language
        
    def run(self):
        file_name = os.path.basename(self.file_path)
        self.log_signal.emit(f"処理開始: {file_name}")
        
        try:
            # ここで実際の文字起こし処理を行う（プロトタイプなのでシミュレーション）
            # 実際の実装では、ここでWhisperを呼び出して音声認識を行う
            for i in range(101):
                self.progress_signal.emit(i)
                self.msleep(20)  # 処理時間をシミュレート
            
            # 仮のテキスト生成（実際の実装ではWhisperの結果を使う）
            transcribed_text = f"{file_name}の文字起こし結果をここに表示します。\n" \
                              f"選択された言語: {self.language}\n" \
                              f"これはテスト用のサンプルテキストです。"
            
            self.log_signal.emit(f"処理完了: {file_name}")
            self.finished_signal.emit(file_name, transcribed_text)
            
        except Exception as e:
            self.log_signal.emit(f"エラー: {file_name} - {str(e)}")


class MP3TranscriberApp(QMainWindow):
    """MP3文字起こしアプリケーションのメインウィンドウ"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP3文字起こしアプリ")
        self.setGeometry(100, 100, 800, 600)
        self.selected_files = []
        self.output_dir = ""
        self.active_threads = []
        self.transcription_results = {}  # ファイル名:テキスト内容
        
        self.init_ui()
        
    def init_ui(self):
        # メインレイアウト
        main_layout = QVBoxLayout()
        
        # ファイル選択エリア
        file_group = QGroupBox("ファイル選択")
        file_layout = QVBoxLayout()
        
        browse_layout = QHBoxLayout()
        self.folder_btn = QPushButton("フォルダ選択")
        self.folder_btn.clicked.connect(self.select_folder)
        self.files_btn = QPushButton("ファイル選択")
        self.files_btn.clicked.connect(self.select_files)
        browse_layout.addWidget(self.folder_btn)
        browse_layout.addWidget(self.files_btn)
        
        self.file_list = QListWidget()
        
        file_layout.addLayout(browse_layout)
        file_layout.addWidget(QLabel("選択されたファイル:"))
        file_layout.addWidget(self.file_list)
        
        file_group.setLayout(file_layout)
        
        # 設定エリア
        settings_group = QGroupBox("設定")
        settings_layout = QGridLayout()
        
        settings_layout.addWidget(QLabel("言語:"), 0, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["日本語", "英語", "中国語", "韓国語", "自動検出"])
        settings_layout.addWidget(self.language_combo, 0, 1)
        
        settings_layout.addWidget(QLabel("出力先:"), 1, 0)
        output_layout = QHBoxLayout()
        self.output_path_label = QLabel("デフォルト: カレントディレクトリ")
        self.output_browse_btn = QPushButton("参照...")
        self.output_browse_btn.clicked.connect(self.select_output_dir)
        output_layout.addWidget(self.output_path_label)
        output_layout.addWidget(self.output_browse_btn)
        settings_layout.addLayout(output_layout, 1, 1)
        
        settings_layout.addWidget(QLabel("出力形式:"), 2, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["テキストファイル (.txt)", "Word文書 (.docx)", "JSONファイル (.json)"])
        settings_layout.addWidget(self.format_combo, 2, 1)
        
        settings_group.setLayout(settings_layout)
        
        # 処理エリア
        process_group = QGroupBox("処理")
        process_layout = QVBoxLayout()
        
        self.start_btn = QPushButton("文字起こし開始")
        self.start_btn.clicked.connect(self.start_transcription)
        self.start_btn.setEnabled(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        process_layout.addWidget(self.start_btn)
        process_layout.addWidget(QLabel("進捗状況:"))
        process_layout.addWidget(self.progress_bar)
        process_layout.addWidget(QLabel("ログ:"))
        process_layout.addWidget(self.log_text)
        
        process_group.setLayout(process_layout)
        
        # レイアウトの組み立て
        main_layout.addWidget(file_group)
        main_layout.addWidget(settings_group)
        main_layout.addWidget(process_group)
        
        # 中央ウィジェットの設定
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def select_folder(self):
        """フォルダを選択し、MP3ファイルを検索"""
        folder_path = QFileDialog.getExistingDirectory(self, "フォルダ選択", "")
        if folder_path:
            self.file_list.clear()
            self.selected_files = []
            
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.mp3'):
                        file_path = os.path.join(root, file)
                        self.selected_files.append(file_path)
                        self.file_list.addItem(file)
            
            if self.selected_files:
                self.start_btn.setEnabled(True)
                self.log_text.append(f"{len(self.selected_files)}個のMP3ファイルが見つかりました。")
            else:
                self.start_btn.setEnabled(False)
                self.log_text.append("MP3ファイルが見つかりませんでした。")
    
    def select_files(self):
        """複数のMP3ファイルを選択"""
        files, _ = QFileDialog.getOpenFileNames(self, "MP3ファイル選択", "", "MP3 Files (*.mp3)")
        if files:
            self.file_list.clear()
            self.selected_files = files
            
            for file in files:
                self.file_list.addItem(os.path.basename(file))
            
            self.start_btn.setEnabled(True)
            self.log_text.append(f"{len(files)}個のファイルが選択されました。")
    
    def select_output_dir(self):
        """出力ディレクトリを選択"""
        dir_path = QFileDialog.getExistingDirectory(self, "出力先フォルダ選択", "")
        if dir_path:
            self.output_dir = dir_path
            self.output_path_label.setText(dir_path)
            self.log_text.append(f"出力先: {dir_path}")
    
    def start_transcription(self):
        """文字起こし処理を開始"""
        if not self.selected_files:
            self.log_text.append("ファイルが選択されていません。")
            return
        
        # 既存のスレッドをクリア
        for thread in self.active_threads:
            if thread.isRunning():
                thread.terminate()
        
        self.active_threads = []
        self.transcription_results = {}
        self.progress_bar.setValue(0)
        
        # 言語設定の取得
        language_map = {
            "日本語": "ja", 
            "英語": "en", 
            "中国語": "zh", 
            "韓国語": "ko", 
            "自動検出": "auto"
        }
        selected_language = language_map[self.language_combo.currentText()]
        
        # 最初のファイルの処理を開始
        self.start_next_file(0, selected_language)
    
    def start_next_file(self, index, language):
        """次のファイルの処理を開始"""
        if index < len(self.selected_files):
            file_path = self.selected_files[index]
            thread = TranscriptionThread(file_path, language)
            thread.progress_signal.connect(self.update_progress)
            thread.log_signal.connect(self.update_log)
            thread.finished_signal.connect(lambda file_name, text: self.handle_transcription_finished(file_name, text, index, language))
            
            self.active_threads.append(thread)
            thread.start()
    
    def update_progress(self, value):
        """進捗バーを更新"""
        self.progress_bar.setValue(value)
    
    def update_log(self, message):
        """ログを更新"""
        self.log_text.append(message)
    
    def handle_transcription_finished(self, file_name, text, current_index, language):
        """文字起こし完了時の処理"""
        # 結果を保存
        self.transcription_results[file_name] = text
        
        # 実際のファイル保存処理
        if self.output_dir:
            output_path = os.path.join(self.output_dir, f"{file_name}.txt")
        else:
            output_path = f"{file_name}.txt"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            self.log_text.append(f"保存完了: {output_path}")
        except Exception as e:
            self.log_text.append(f"ファイル保存エラー: {str(e)}")
        
        # 次のファイルを処理
        next_index = current_index + 1
        if next_index < len(self.selected_files):
            self.start_next_file(next_index, language)
        else:
            self.log_text.append("全ファイルの処理が完了しました。")


def main():
    app = QApplication(sys.argv)
    window = MP3TranscriberApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()