# Demucs 音源分離ツール

音楽ファイルを6つのトラック（ボーカル、ドラム、ベース、ギター、ピアノ、その他）に分離するPythonラッパーツールです。

## 必要な環境

- Python 3.10 以上
- FFmpeg

## セットアップ

### 1. inputフォルダの作成

まず、音楽ファイルを配置するフォルダを作成します。

```bash
mkdir input
```

> **Note**: このフォルダがないとエラーになります。必ず最初に作成してください。

### 2. 依存関係のインストール

```bash
pip3 install -r requirements.txt
```

### 3. 実行権限の付与

```bash
chmod +x run.sh
```

## 使い方

### 基本的な使い方（3ステップ）

#### ステップ1: 音楽ファイルを配置

音楽ファイルを`input`フォルダにコピーします。

**方法1: コマンドラインでコピー**
```bash
cp ~/Music/your_song.mp3 input/
```

**方法2: Finderでコピー（Mac）**
1. Finderで`demucs-test`フォルダを開く
2. `input`フォルダを開く
3. 音楽ファイルをドラッグ&ドロップ

**方法3: エクスプローラーでコピー（Windows）**
1. エクスプローラーで`demucs-test`フォルダを開く
2. `input`フォルダを開く
3. 音楽ファイルをドラッグ&ドロップ

#### ステップ2: スクリプトを実行

**方法1: シェルスクリプトで実行（推奨・簡単）**
```bash
./run.sh your_song.mp3
```

**方法2: Pythonスクリプトで実行**
```bash
python3 scripts/separate.py input/your_song.mp3
```

> **Note**: ファイル名にスペースが含まれる場合は、クォートで囲んでください。
> ```bash
> ./run.sh "My Song.mp3"
> ```

#### ステップ3: 結果を確認

`output/htdemucs_6s/your_song/` に以下のファイルが生成されます:

### 出力ファイル

#### 分離トラック（6ファイル）
- `vocals.mp3` - ボーカル
- `drums.mp3` - ドラム
- `bass.mp3` - ベース
- `guitar.mp3` - ギター
- `piano.mp3` - ピアノ・キーボード
- `other.mp3` - その他（シンセ・電子音など）

#### ミックストラック（2ファイル）
- `no_drums.mp3` - ドラム抜き（vocals + bass + guitar + piano + other）
- `piano_other.mp3` - ピアノ+その他のみ（piano + other）

## ディレクトリ構造

```
demucs-test/
├── input/              # 元の音楽ファイルを配置
├── output/             # 分離結果の出力先
│   └── htdemucs_6s/   # モデル名のフォルダ
│       └── 曲名/       # 各曲ごとのフォルダ
│           ├── vocals.mp3
│           ├── drums.mp3
│           ├── bass.mp3
│           ├── guitar.mp3
│           ├── piano.mp3
│           ├── other.mp3
│           ├── no_drums.mp3
│           └── piano_other.mp3
├── temp/               # 一時ファイル（自動削除）
├── scripts/
│   └── separate.py
├── function_demucs.py
└── run.sh
```

## 実行例

### 例1: 基本的な実行

```bash
./run.sh "シュガーソングとビターステップ.m4a"
```

### 例2: Pythonスクリプトで直接実行

```bash
python3 scripts/separate.py input/your_song.mp3
```

## カスタマイズ

### プログラムから使う場合

```python
from function_demucs import demucs_separate, mix_specific_stems, Model

# 音源分離を実行
output_dir = demucs_separate("input/song.mp3", model_name=Model.htdemucs_6s)

# カスタムミックスを作成
# 例: ベースとドラムだけのミックス
mix_specific_stems(output_dir, ["bass", "drums"], "bass_drums")

# 例: ボーカル抜き
all_stems = ["vocals", "drums", "bass", "guitar", "piano", "other"]
no_vocals = [s for s in all_stems if s != "vocals"]
mix_specific_stems(output_dir, no_vocals, "no_vocals")
```

### 利用可能なステム

- `vocals` - ボーカル
- `drums` - ドラム
- `bass` - ベース
- `guitar` - ギター
- `piano` - ピアノ
- `other` - その他

## トラブルシューティング

### ffmpegが見つからない

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### Pythonのバージョンが古い

```bash
python3 --version  # 3.10以上であることを確認
```

### 依存関係のエラー

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## 技術情報

- **使用モデル**: htdemucs_6s (6トラック分離)
- **出力フォーマット**: MP3
- **音源分離エンジン**: Meta Demucs
- **音声処理**: pydub + FFmpeg

## ライセンス

このツールは Demucs ライブラリのラッパーです。Demucs のライセンスに従います。
