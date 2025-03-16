# mp3-transcriber
mp3 to text
# MP3文字起こしアプリケーション

ローカルPC上のMP3形式の音声ファイルを、テキストデータに自動で変換するPython/PyQtアプリケーションです。

## 機能

- フォルダまたは個別ファイル選択による複数MP3ファイルの処理
- 音声認識による自動文字起こし
- 複数言語対応（日本語、英語、中国語、韓国語、自動検出）
- 処理の進捗状況表示
- テキストファイル（将来的にはWord, JSON形式）での出力

## セットアップ

### 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

### インストール手順

1. リポジトリのクローンまたはファイルのダウンロード

```bash
git clone https://github.com/yourusername/mp3-transcriber.git
cd mp3-transcriber
```

2. 仮想環境の作成 (オプションですが推奨)

```bash
cd /path/to/repo
uv init
```

3. 必要なパッケージのインストール

```bash
uv add PyQt5==5.15.9 openai-whisper==20231117 torch==2.2.0 numpy==1.26.3 python-docx==1.0.1t
```

## 使用方法

1. アプリケーションの起動

```bash
python mp3_transcriber.py
```

2. 「フォルダ選択」または「ファイル選択」ボタンで音声ファイルを選択

3. 必要に応じて以下を設定:
   - 言語選択
   - 出力先フォルダ
   - 出力形式

4. 「文字起こし開始」ボタンをクリックして処理を開始

5. 進捗バーとログから処理状況を確認

6. 処理完了後、指定の出力先にテキストファイルが生成されます

## 注意事項

- プロトタイプバージョンでは、音声認識処理はシミュレーションのみで、実際の文字起こしは行われません
- 実際の音声認識機能を有効にするには、Whisperモデルの統合が必要です（次のバージョンで実装予定）

## 今後の実装予定機能

- OpenAI Whisperモデルの統合による実際の音声認識機能
- Word文書、JSON形式での出力サポート
- 認識精度の調整オプション
- バッチ処理の一時停止・再開機能
- エラーリカバリと再試行機能
- ユーザー辞書による専門用語対応

```bash future plan
mp3-transcriber/
├── main.py           # アプリケーションのエントリーポイント
├── ui/               # UIコンポーネント
│   ├── main_window.py
│   └── progress.py
├── core/             # 核となる機能
│   ├── file_handler.py
│   ├── transcriber.py
│   └── output_formatter.py
├── models/           # Whisperモデル用ディレクトリ 
├── output/           # デフォルト出力ディレクトリ
└── logs/             # ログディレクトリ
```

## 開発者向け情報

このアプリケーションは以下のコンポーネントで構成されています：

- **MP3TranscriberApp**: メインのアプリケーションウィンドウとUI管理
- **TranscriptionThread**: 音声文字起こし処理を行う独立スレッド

拡張開発を行う場合は、以下のファイルを修正してください：

- **mp3_transcriber.py**: メインアプリケーションコード
- **requirements.txt**: 依存パッケージリスト

## ライセンス

MIT License