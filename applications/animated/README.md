# MontageSubs · animated logo

Embed the neon-turn-on animation in any markdown file:

```markdown
![MontageSubs neon on](applications/animated/animated-neon-on.svg)
```

Or in HTML:

```html
<img src="applications/animated/animated-neon-on.svg" alt="MontageSubs">
```

The SVG plays its 2.5s "neon turn-on" sequence once on each page load.
For a continuous loop, wrap in CSS that periodically reloads or use the
animated GIF version (run `python3 .tools/render_animated_gif.py`).

For video footage (片头/片尾 use), the recommended workflow:
1. Open `animated-neon-on.html` in a browser
2. Use a screen recorder (e.g., Quicktime, OBS, ffmpeg) to capture the 2.5s
3. Encode to ProRes or H.264 with transparent alpha if your editor supports it
