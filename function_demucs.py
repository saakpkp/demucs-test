import demucs.separate as ds
import ffmpeg, os, enum #ffmpeg-python
from pydub import AudioSegment

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
    convert_path = os.path.dirname(__file__)+"/sample/"+os.path.basename(track)
    if convert_path.endswith(".wav"):
        pass
    else:
        convert_path = convert_path.split(".")[0]+".wav"

    try:
        ffmpeg_input =  ffmpeg.input(track)
        ffmpeg_output = ffmpeg.output(ffmpeg_input, convert_path)
        ffmpeg.run(ffmpeg_output, overwrite_output=True)
    except:
        print("[Error] ffmpeg convert error")

    else: # create options
        options = [convert_path]
        if model_name and isinstance(model_name, Model):
            options.extend(["-n", model_name])
        elif stem and isinstance(stem, Stem):
            options.extend(["--two-stems", stem])
        elif format and isinstance(format, Format):
            options.extend(["--"+format])
        print(f"[Options]:{options}")
        ds.main(options)

def mix_without_stem(separated_dir, exclude_stem):
    """
    指定したステムを除いた音源をミックスする

    Args:
        separated_dir: 分離されたファイルがあるディレクトリ (例: "separated/htdemucs/曲名")
        exclude_stem: 除外するステム ("drums" or "vocals" or "bass" or "other")

    Returns:
        作成されたファイルのパス
    """
    stems = ["vocals", "drums", "bass", "other"]

    if exclude_stem not in stems:
        print(f"[Error] 無効なステム名: {exclude_stem}")
        return None

    stems.remove(exclude_stem)

    # 最初のトラックを読み込み
    first_track_path = os.path.join(separated_dir, f"{stems[0]}.mp3")
    if not os.path.exists(first_track_path):
        print(f"[Error] ファイルが見つかりません: {first_track_path}")
        return None

    mixed = AudioSegment.from_file(first_track_path)
    print(f"[Mix] ベース: {stems[0]}")

    # 残りのトラックを重ねる
    for stem in stems[1:]:
        track_path = os.path.join(separated_dir, f"{stem}.mp3")
        if os.path.exists(track_path):
            track = AudioSegment.from_file(track_path)
            mixed = mixed.overlay(track)
            print(f"[Mix] 追加: {stem}")
        else:
            print(f"[Warning] スキップ: {stem} (ファイルが見つかりません)")

    # 出力ファイル名
    output_path = os.path.join(separated_dir, f"no_{exclude_stem}.mp3")
    mixed.export(output_path, format="mp3")
    print(f"[完了] {output_path}")

    return output_path

if __name__ == "__main__":
    demucs_separate("")