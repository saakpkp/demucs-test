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

from function_demucs import demucs_separate, mix_specific_stems, Model

def main():
    # コマンドライン引数からファイルパスを取得
    if len(sys.argv) < 2:
        print("使い方: python3 scripts/separate.py input/your_song.mp3")
        sys.exit(1)

    input_file = sys.argv[1]

    # ファイル名（拡張子なし）を取得
    filename = Path(input_file).stem

    print(f"🎵 音源分離を開始: {filename}")

    # 音源分離を実行（6トラックモデル使用）
    output_dir = demucs_separate(input_file, model_name=Model.htdemucs_6s)

    if not output_dir:
        print("❌ 音源分離に失敗しました")
        sys.exit(1)

    print(f"\n🥁 ドラム抜きを作成中...")
    all_stems = ["vocals", "drums", "bass", "guitar", "piano", "other"]
    no_drums = [s for s in all_stems if s != "drums"]
    mix_specific_stems(output_dir, no_drums, "no_drums")

    print(f"\n🎹 ピアノ+その他ミックスを作成中...")
    mix_specific_stems(output_dir, ["piano", "other"], "piano_other")

    print(f"\n✅ 完了！結果: {output_dir}/")
    print(f"📁 分離トラック: vocals.mp3, drums.mp3, bass.mp3, guitar.mp3, piano.mp3, other.mp3")
    print(f"📁 ミックス: no_drums.mp3, piano_other.mp3")

if __name__ == "__main__":
    main()
