#!/usr/bin/env bash
# assemble.sh <paras_dir> <bed.wav> <out.mp3>
# Intro music (Breton tune, starts at 0 s) at full level for 6.5 s (the tune resolves at 6 s), ducks to
# about -16 dB between 6.5 and 7.5 s, voice starts at 7.2 s, music fades out from 16 to 21 s.
# Outro: the first 9 s of the bed come back softly after the voice.
set -euo pipefail
PARAS=$1; BED=$2; OUT=$3
WORK=$(mktemp -d)
ls "$PARAS"/p*.wav | sed "s/.*/file '&'/" > "$WORK/vlist.txt"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$WORK/vlist.txt" -ar 44100 "$WORK/voice.wav"
VD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$WORK/voice.wav")
END_MS=$(python3 -c "print(int(($VD + 7.2 + 0.4) * 1000))")
TOTAL=$(python3 -c "print(round($VD + 7.2 + 0.4 + 7.5, 2))")
ffmpeg -y -loglevel error -i "$BED" -i "$BED" -i "$WORK/voice.wav" -filter_complex "\
[0:a]volume='if(lt(t,6.5),1,if(lt(t,7.5),1-(t-6.5)*0.84,if(lt(t,16),0.16,if(lt(t,21),0.16*(21-t)/5,0))))':eval=frame,atrim=0:22[intro];\
[1:a]atrim=0:7,afade=t=out:st=5.5:d=1.5,volume=0.75,adelay=${END_MS}|${END_MS}[outro];\
[2:a]adelay=7200,apad[v];\
[intro][v][outro]amix=inputs=3:duration=longest:normalize=0,highpass=f=40,loudnorm=I=-16[o]" \
  -map "[o]" -t "$TOTAL" -c:a libmp3lame -b:a 128k "$OUT"
rm -rf "$WORK"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
