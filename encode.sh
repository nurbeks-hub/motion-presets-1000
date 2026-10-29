#!/bin/bash
# web previews of lib1000 finals: 480 px short side, CRF 30, no audio; chroma presets are keyed over the dark studio
# backdrop (#141418) like the covers — the delivered finals stay on chroma blue. Skips done ones (FORCE_CHROMA=1 redoes keyed).
F=/Users/nurbek.s/Documents/Claude/2026-10-28/motion-library/lib1000/finals
O=/Users/nurbek.s/Projects/presets-1000-site/media
CH=/Users/nurbek.s/Projects/presets-1000-site/chroma_ids.txt
enc() {
  f="$1"; n=$(basename "$f" .mp4)
  key=0; grep -qx "$n" "$CH" && key=1
  [ -s "$O/$n.mp4" ] && ! { [ "$key" = 1 ] && [ "$FORCE_CHROMA" = 1 ] && [ ! -e "$O/$n.keyed" ]; } && return
  wh=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f"); w=${wh%x*}
  if [ "$w" -lt 1200 ]; then s=480:854; else s=640:480; fi
  if [ "$key" = 1 ]; then
    ffmpeg -nostdin -v error -y -i "$f" -f lavfi -i "color=c=0x141418:s=$wh:r=24" -filter_complex "[0:v]colorkey=0x0047BB:0.13:0.06,despill=type=blue[k];[1:v][k]overlay=shortest=1,scale=$s:flags=lanczos" \
      -c:v libx264 -preset medium -crf 30 -pix_fmt yuv420p -profile:v high -an -movflags +faststart "$O/$n.tmp.mp4" && mv "$O/$n.tmp.mp4" "$O/$n.mp4" && touch "$O/$n.keyed"
  else
    ffmpeg -nostdin -v error -y -i "$f" -vf "scale=$s:flags=lanczos" -c:v libx264 -preset medium -crf 30 -pix_fmt yuv420p -profile:v high -an -movflags +faststart "$O/$n.tmp.mp4" && mv "$O/$n.tmp.mp4" "$O/$n.mp4"
  fi
}
export -f enc; export O CH FORCE_CHROMA
ls $F/*.mp4 | xargs -P 6 -I{} bash -c 'enc "$@"' _ {}
ls "$O"/*.mp4 | wc -l; du -sh "$O"
