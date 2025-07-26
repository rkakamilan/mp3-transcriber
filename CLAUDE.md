# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

このファイルは、このリポジトリでコードを扱う際のClaude Code (claude.ai/code) への指針を提供します。

## Project Overview / プロジェクト概要

This is an MP3 transcription application built with Python and PyQt5 that converts audio files to text using OpenAI's Whisper model. The main application (`main.py`) provides a GUI for batch processing MP3 files with multi-language support and various output formats.

このプロジェクトは、PythonとPyQt5で構築されたMP3文字起こしアプリケーションで、OpenAIのWhisperモデルを使用して音声ファイルをテキストに変換します。メインアプリケーション（`main.py`）は、マルチ言語対応と様々な出力形式でMP3ファイルをバッチ処理するGUIを提供します。

## Development Setup / 開発環境セットアップ

### Dependencies and Package Management / 依存関係とパッケージ管理
- Uses `uv` as the package manager (modern Python dependency management)
- Dependencies are defined in `pyproject.toml` 
- Key dependencies: PyQt5, openai-whisper, torch, numpy, python-docx

- パッケージマネージャーとして`uv`を使用（モダンなPython依存関係管理）
- 依存関係は`pyproject.toml`で定義
- 主要依存関係: PyQt5, openai-whisper, torch, numpy, python-docx

### Installation Commands / インストールコマンド
```bash
# Install dependencies / 依存関係をインストール
uv sync

# Run the application / アプリケーションを実行
python main.py

# Test Whisper installation / Whisperインストールをテスト
python test_whisper.py
```

## Architecture / アーキテクチャ

### Core Components / コアコンポーネント
- `main.py`: Main application with PyQt5 GUI (MP3TranscriberApp class)
- `WhisperTranscriptionThread`: QThread class for background audio processing
- `model.py`: Contains an alternative implementation of the transcription thread
- `mp3-transcriber-prototype.py`: Earlier prototype version

- `main.py`: PyQt5 GUIを持つメインアプリケーション（MP3TranscriberAppクラス）
- `WhisperTranscriptionThread`: バックグラウンド音声処理用のQThreadクラス
- `model.py`: 文字起こしスレッドの代替実装を含む
- `mp3-transcriber-prototype.py`: 初期プロトタイプバージョン

### Key Classes and Patterns / 主要クラスとパターン
- **MP3TranscriberApp**: Main window class with comprehensive UI management
- **WhisperTranscriptionThread**: Handles Whisper model loading and transcription in background
- Uses PyQt5's signal/slot pattern for thread communication:
  - `progress_signal`: Progress updates (int)
  - `log_signal`: Log messages (str) 
  - `finished_signal`: Completion with results (str, str)
  - `error_signal`: Error handling (str, str)

- **MP3TranscriberApp**: 包括的なUI管理を持つメインウィンドウクラス
- **WhisperTranscriptionThread**: Whisperモデル読み込みとバックグラウンド文字起こしを処理
- スレッド通信にPyQt5のsignal/slotパターンを使用:
  - `progress_signal`: 進捗更新 (int)
  - `log_signal`: ログメッセージ (str) 
  - `finished_signal`: 結果付き完了 (str, str)
  - `error_signal`: エラー処理 (str, str)

### File Processing Flow / ファイル処理フロー
1. User selects files/folders through GUI
2. Files are processed sequentially (not parallel) by `start_next_file()` method
3. Each file creates a new `WhisperTranscriptionThread` instance
4. Results are saved in multiple formats (txt, docx, json) based on user selection
5. Comprehensive logging to both GUI and log files

1. ユーザーがGUIを通じてファイル/フォルダを選択
2. `start_next_file()`メソッドによりファイルを順次処理（並列処理ではない）
3. 各ファイルに対して新しい`WhisperTranscriptionThread`インスタンスを作成
4. ユーザー選択に基づいて複数形式（txt, docx, json）で結果を保存
5. GUIとログファイル両方への包括的ログ記録

### Logging System / ログシステム
- Comprehensive logging setup with both file and console handlers
- Log files stored in `logs/` directory with timestamp format
- Global exception handler configured
- Japanese language support in log messages

- ファイルハンドラーとコンソールハンドラー両方を持つ包括的ログ設定
- ログファイルは`logs/`ディレクトリにタイムスタンプ形式で保存
- グローバル例外ハンドラーを設定
- ログメッセージでの日本語サポート

### UI Features / UI機能
- Multi-language support (Japanese, English, Chinese, Korean, auto-detection)
- Multiple Whisper model sizes (tiny, base, small, medium, large)
- Multiple output formats (txt, docx, json)
- Progress tracking and real-time log display
- Debug mode toggle

- マルチ言語サポート（日本語、英語、中国語、韓国語、自動検出）
- 複数のWhisperモデルサイズ（tiny, base, small, medium, large）
- 複数の出力形式（txt, docx, json）
- 進捗追跡とリアルタイムログ表示
- デバッグモード切り替え

## Important Notes / 重要事項

### Thread Safety / スレッドセーフティ
- Only one transcription runs at a time (sequential processing)
- Proper thread cleanup in `cancel_transcription()`
- UI state management during processing

- 一度に一つの文字起こしのみ実行（順次処理）
- `cancel_transcription()`での適切なスレッドクリーンアップ
- 処理中のUI状態管理

### Error Handling / エラー処理
- Comprehensive exception handling throughout
- Graceful fallbacks (e.g., txt output if docx fails)
- User-friendly error messages in Japanese

- 全体を通じた包括的例外処理
- 優雅なフォールバック（例：docx失敗時のtxt出力）
- 日本語でのユーザーフレンドリーなエラーメッセージ

### Model Management / モデル管理
- Whisper models are loaded per-thread basis
- Supports GPU/CPU automatic detection
- Model size selection affects accuracy vs speed tradeoff

- Whisperモデルはスレッド単位で読み込み
- GPU/CPU自動検出をサポート
- モデルサイズ選択は精度と速度のトレードオフに影響

### Output Handling / 出力処理
- Metadata included in all output formats (filename, language, model used)
- JSON output separates metadata from content
- DOCX output requires python-docx library with fallback to txt

- 全出力形式にメタデータを含む（ファイル名、言語、使用モデル）
- JSON出力はメタデータとコンテンツを分離
- DOCX出力にはpython-docxライブラリが必要（txtへのフォールバック付き）