# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

このリポジトリは Demucs（音源分離ライブラリ）の Python ラッパーです。音楽トラックをボーカル、ドラム、ベース、その他の楽器に分離する機能を提供します。

## ディレクトリ構造

```
demucs-test/
├── input/              # 元の音楽ファイルを配置
├── output/             # 分離結果の出力先（将来的な拡張用）
├── separated/          # Demucsが自動生成する出力ディレクトリ
│   └── htdemucs/      # モデル名のフォルダ
│       └── 曲名/       # 各曲ごとのフォルダ
│           ├── vocals.mp3      # 分離されたボーカル
│           ├── drums.mp3       # 分離されたドラム
│           ├── bass.mp3        # 分離されたベース
│           ├── other.mp3       # 分離されたその他
│           ├── no_drums.mp3    # ドラム抜きミックス
│           └── no_vocals.mp3   # ボーカル抜きミックス
├── sample/             # 一時的なWAV変換ファイル用
├── scripts/            # 実行用スクリプト
│   └── separate.py    # メインの音源分離スクリプト
├── function_demucs.py  # コア機能（音源分離・ミックス関数）
├── test_demucs.py      # 簡易テスト用スクリプト
└── run.sh              # 簡易実行用シェルスクリプト
```

## 環境構築

```bash
# 依存関係のインストール
pip install -r requirements.txt

# または Pipenv を使用
pipenv install
pipenv shell
```

**必須**: Python 3.10 以上

## 主要な実行コマンド

### 推奨: シェルスクリプトで実行（最も簡単）
```bash
# 1. 音楽ファイルをinputフォルダに配置
cp ~/Music/your_song.mp3 input/

# 2. スクリプトを実行
./run.sh your_song.mp3

# 結果は separated/htdemucs/your_song/ に出力される
```

### Pythonスクリプトで直接実行
```bash
python3 scripts/separate.py input/your_song.mp3
```

### テストスクリプトの実行（レガシー）
```bash
# test_demucs.py を編集してパスを指定後
python3 test_demucs.py
```

### 関数として使用（プログラマティックな利用）
```python
from function_demucs import demucs_separate, mix_without_stem, Model, Format

# 音源分離
demucs_separate("path/to/audio.mp3", model_name=Model.htdemucs, format=Format.mp3)

# ミックス作成
mix_without_stem("separated/htdemucs/曲名", "drums")   # ドラム抜き
mix_without_stem("separated/htdemucs/曲名", "vocals")  # ボーカル抜き
```

## アーキテクチャ

### コアファイル構成

- **function_demucs.py**: メインロジック
  - `demucs_separate()`: 音源分離のエントリーポイント
  - 処理フロー:
    1. ffmpeg で入力音声を WAV 形式に変換
    2. `sample/` ディレクトリに一時ファイル保存
    3. `demucs.separate.main()` を options 配列で呼び出し
    4. 分離結果は `separated/{model_name}/` に出力

- **test_demucs.py**: 動作確認用スクリプト
  - `demucs.separate.main()` を直接呼び出す簡易テスト

### 重要な設定パターン

**Options 配列の構築ルール**:
- モデル指定: `["-n", model_name]`
- ステム指定（2トラック分離）: `["--two-stems", stem]`
- フォーマット指定: `["--{format}"]` (例: `--mp3`)
- これらは排他的ではなく、組み合わせ可能

### 依存関係

- **demucs**: Meta の音源分離ライブラリ（本体）
- **ffmpeg-python**: 音声フォーマット変換
  - システムに ffmpeg バイナリが必要

## 出力ディレクトリ構造

```
separated/
  └── {model_name}/     # 例: htdemucs/
      └── {track_name}/
          ├── vocals.mp3
          ├── drums.mp3
          ├── bass.mp3
          └── other.mp3
```

## 注意事項

- `sample/` ディレクトリが存在する前提（コード内でディレクトリ作成処理なし）
- ffmpeg 変換エラーは try-except でキャッチされるが、失敗時は Demucs 実行をスキップ
- 入力ファイルパスは絶対パス推奨（test_demucs.py 参照）
