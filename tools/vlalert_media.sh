#!/usr/bin/env bash
# VLAlert demo media for the lab showcase: GIF -> MP4 (H.264, faststart) with full-width redaction bars over the bands that
# carry third-party identifiers in the source dashcam uploads (platform watermark, uploader handle/avatar, date/VIN strip).
# Usage: tools/vlalert_media.sh /path/to/WangYuHang-cmd.github.io/vlalert/static/images  content/projects/vlalert/static/media
set -euo pipefail
SRC="$1"; OUT="$2"; mkdir -p "$OUT"
conv() { # name  drawbox-filter-chain
  local n="$1" boxes="$2"
  ffmpeg -v error -y -i "$SRC/$n.gif" -vf "${boxes}scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p" -r 10 -an \
    -c:v libx264 -preset slow -crf 30 -movflags +faststart "$OUT/$n.mp4"
  ffmpeg -v error -y -ss 6 -i "$OUT/$n.mp4" -frames:v 1 -q:v 4 "$OUT/$n.jpg"
  printf "%s  %s bytes  poster %s bytes\n" "$n" "$(stat -c%s "$OUT/$n.mp4")" "$(stat -c%s "$OUT/$n.jpg")"
}
# demo1 520x440: top band (watermark + handle) and the dashcam date/speed/VIN strip above the chart
conv vlalert_demo1 "drawbox=x=0:y=27:w=iw:h=47:color=black@1:t=fill,drawbox=x=0:y=283:w=iw:h=34:color=black@1:t=fill,"
# demo3 560x474: watermark/handle alternate between the top and bottom bands of the video area; timestamp at the bottom edge
conv vlalert_demo3 "drawbox=x=0:y=27:w=iw:h=49:color=black@1:t=fill,drawbox=x=0:y=286:w=iw:h=61:color=black@1:t=fill,"
# demo9 520x371: no overlays in the source
conv vlalert_demo9 ""
