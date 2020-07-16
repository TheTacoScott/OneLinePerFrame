#!/bin/bash
ffmpeg -i "$1" -vf "scale=1.2*iw:-1" -vf "crop=iw/1.2:ih/1.2" -vf "eq=brightness=0.1" -vf "scale=16:16:flags=fast_bilinear" -f image2pipe -vcodec png -an - 2>/dev/null | ./one_line_per_frame.py --output "$2" --height 4800 --width 6000
