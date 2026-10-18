#!/usr/bin/env bash
# assemble.sh <paras_dir> <bed.wav> <out.mp3>
# Intro music at full level for 8.5 s (the Marseillaise phrase ends ~8 s), ducks to about -16 dB
# between 8.5 and 9.5 s, voice starts at 9.2 s, music fades out from 18 to 23 s.
# Outro: the first 9 s of the bed come back softly after the voice.
set -euo pipefail
PARAS=$1; BED=$2; OUT=$3
WORK=$(mktemp -d)
ls "$PARAS"/p*.wav | sed "s/.*/file '&'/" > "$WORK/vlist.txt"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$WORK/vlist.txt" -ar 44100 "$WORK/voice.wav"
VD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$WORK/voice.wav")
END_MS=$(python3 -c "print(int(($VD + 9.2 + 0.4) * 1000))")
TOTAL=$(python3 -c "print(round($VD + 9.2 + 0.4 + 9.5, 2))")
ffmpeg -y -loglevel error -i "$BED" -i "$BED" -i "$WORK/voice.wav" -filter_complex "\
[0:a]volume='if(lt(t,8.5),1,if(lt(t,9.5),1-(t-8.5)*0.84,if(lt(t,18),0.16,if(lt(t,23),0.16*(23-t)/5,0))))':eval=frame,atrim=0:24[intro];\
[1:a]atrim=0:9,afade=t=out:st=7.5:d=1.5,volume=0.75,adelay=${END_MS}|${END_MS}[outro];\
[2:a]adelay=9200,apad[v];\
[intro][v][outro]amix=inputs=3:duration=longest:normalize=0,highpass=f=40,loudnorm=I=-16[o]" \
  -map "[o]" -t "$TOTAL" -c:a libmp3lame -b:a 128k "$OUT"
rm -rf "$WORK"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
