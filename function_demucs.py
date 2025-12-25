import demucs.separate as ds
import ffmpeg, os, enum, shutil #ffmpeg-python
from pydub import AudioSegment
from pathlib import Path

class Model(enum.Enum):
    htdemucs = "htdemucs"
    htdemucs_ft = "htdemucs_ft"
    htdemucs_6s = "htdemucs_6s"
    hdemucs_mmi = "hdemucs_mmi"
    mdx = "mdx"
    mdx_extra = "mdx_extra"
    mdx_q = "mdx_q"

class Stem(enum.Enum):
    vocals = "vocals"
    drums = "drums"
    bass = "bass"
    other = "other"

class Format(enum.Enum):
    int24 = "int24"
    float32 = "float32"
    mp3 = "mp3"
    flac = "flac"

def demucs_separate(track, model_name:Model=None, stem:Stem=None, format:Format=None):
    """
    音源分離を実行し、output/htdemucs/曲名/ ディレクトリに結果を出力する

    Args:
        track: 入力音声ファイルのパス
        model_name: 使用するモデル
        stem: ステム指定（2トラック分離用）
        format: 出力フォーマット

    Returns:
        出力ディレクトリのパス (output/htdemucs/曲名/)
    """
    # プロジェクトルートと曲名を取得
    project_root = Path(__file__).parent
    track_name = Path(track).stem

    # 一時ディレクトリを作成（WAV変換用）
    temp_dir = project_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # 一時WAV変換ファイルのパス
    temp_wav = temp_dir / f"{track_name}.wav"

    # FFmpegでWAVに変換
    try:
        ffmpeg_input = ffmpeg.input(track)
        ffmpeg_output = ffmpeg.output(ffmpeg_input, str(temp_wav))
        ffmpeg.run(ffmpeg_output, overwrite_output=True, quiet=True)
        print(f"[Convert] WAV変換完了: {temp_wav.name}")
    except Exception as e:
        print(f"[Error] ffmpeg変換エラー: {e}")
        return None

    # Demucsのオプションを構築
    model = model_name.value if model_name else "htdemucs"
    output_base = project_root / "output"

    options = [
        str(temp_wav),
        "-o", str(output_base),
        "-n", model,
        "--mp3"  # デフォルトでMP3出力
    ]

    if stem and isinstance(stem, Stem):
        options.extend(["--two-stems", stem.value])

    print(f"[Demucs] 音源分離を開始...")
    print(f"[Options] {' '.join(options)}")

    # Demucsで音源分離を実行（output/htdemucs/曲名/ に自動出力）
    ds.main(options)

    # 一時WAVファイルを削除
    if temp_wav.exists():
        temp_wav.unlink()
        print(f"[Clean] 一時ファイルを削除: {temp_wav.name}")

    # 一時ディレクトリを削除（空の場合）
    if temp_dir.exists() and not list(temp_dir.iterdir()):
        temp_dir.rmdir()

    # 最終的な出力ディレクトリのパス
    final_output = output_base / model / track_name
    return str(final_output)

def mix_specific_stems(output_dir, stem_list, output_filename=None):
    """
    指定したステムだけをミックスする

    Args:
        output_dir: 分離されたファイルがあるディレクトリ (例: "output/htdemucs_6s/曲名")
        stem_list: ミックスするステムのリスト (例: ["piano", "other"])
        output_filename: 出力ファイル名（拡張子なし）。指定しない場合は自動生成

    Returns:
        作成されたファイルのパス
    """
    output_path = Path(output_dir)
    all_stems = ["vocals", "drums", "bass", "guitar", "piano", "other"]

    # バリデーション
    if not stem_list:
        print(f"[Error] ステムリストが空です")
        return None

    for stem in stem_list:
        if stem not in all_stems:
            print(f"[Error] 無効なステム名: {stem}")
            return None

    # 最初のトラックを読み込み
    first_track_path = output_path / f"{stem_list[0]}.mp3"
    if not first_track_path.exists():
        print(f"[Error] ファイルが見つかりません: {first_track_path}")
        return None

    mixed = AudioSegment.from_file(str(first_track_path))
    print(f"[Mix] ベース: {stem_list[0]}")

    # 残りのトラックを重ねる
    for stem in stem_list[1:]:
        track_path = output_path / f"{stem}.mp3"
        if track_path.exists():
            track = AudioSegment.from_file(str(track_path))
            mixed = mixed.overlay(track)
            print(f"[Mix] 追加: {stem}")
        else:
            print(f"[Warning] スキップ: {stem} (ファイルが見つかりません)")

    # 出力ファイル名
    if output_filename:
        output_file = output_path / f"{output_filename}.mp3"
    else:
        # ステム名を結合して自動生成 (例: "piano_other.mp3")
        output_file = output_path / f"{'_'.join(stem_list)}.mp3"

    mixed.export(str(output_file), format="mp3")
    print(f"[完了] {output_file.name}")

    return str(output_file)

if __name__ == "__main__":
    demucs_separate("")