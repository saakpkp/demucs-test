#!/usr/bin/env python3
"""
音源分離スクリプト
使い方: python3 scripts/separate.py input/your_song.mp3
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加（importできるようにする）
sys.path.insert(0, str(Path(__file__).parent.parent))

from function_demucs import demucs_separate, mix_without_stem, Model, Format

def main():
    # コマンドライン引数からファイルパスを取得
    if len(sys.argv) < 2:
        print("使い方: python3 scripts/separate.py input/your_song.mp3")
        sys.exit(1)

    input_file = sys.argv[1]

    # ファイル名（拡張子なし）を取得
    filename = Path(input_file).stem

    print(f"🎵 音源分離を開始: {filename}")

    # 音源分離を実行
    demucs_separate(input_file, model_name=Model.htdemucs, format=Format.mp3)

    # 分離されたファイルのディレクトリ
    separated_dir = f"separated/htdemucs/{filename}"

    print(f"🥁 ドラム抜きを作成中...")
    mix_without_stem(separated_dir, "drums")

    print(f"🎤 ボーカル抜きを作成中...")
    mix_without_stem(separated_dir, "vocals")

    print(f"✅ 完了！結果: {separated_dir}/")

if __name__ == "__main__":
    main()
