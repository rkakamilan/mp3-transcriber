try:
    print("Whisperのインポートを試みます...")
    import whisper
    print("Whisperのインポートに成功しました！")
    print("バージョン情報:", whisper.__version__ if hasattr(whisper, "__version__") else "不明")
    
    print("\nTorchのインポートを試みます...")
    import torch
    print("Torchのインポートに成功しました！")
    print("バージョン情報:", torch.__version__)
    print("CUDA利用可能:", torch.cuda.is_available())
    
    # 最小モデルのロードを試みる
    print("\n最小モデル(tiny)のロードを試みます...")
    model = whisper.load_model("tiny")
    print("モデルのロードに成功しました！")
    
except Exception as e:
    print("エラーが発生しました:")
    print(str(e))
    import traceback
    traceback.print_exc()