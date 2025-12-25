#!/bin/bash
# 簡単に実行できるラッパースクリプト
# 使い方: ./run.sh your_song.mp3

if [ $# -eq 0 ]; then
    echo "使い方: ./run.sh 曲ファイル名.mp3"
    echo "例: ./run.sh your_song.mp3"
    exit 1
fi

python3 scripts/separate.py "input/$1"
