"""
Discoveries Tab — Full Page
"🎉 I Never Knew That"
All figures computed from the Anglosphere Baby Names dataset (1997–2023).
Visuals are custom soundwave / multitrack / fader graphics (no plain charts).
"""
import streamlit as st


# ══════════════════════════════════════════════════════════════════
# Reusable creative visuals (pure SVG/HTML — music-themed)
# ══════════════════════════════════════════════════════════════════

def soundwave(values, years, color, peak_emoji="🔊", height=150,
              event_year=None, event_label=""):
    """A mirrored audio waveform: each year is a bar above & below a centre line.
    The peak year's bar is highlighted. Reads as a 'sound clip' of the name's life."""
    n = len(values)
    maxv = max(values) or 1
    peak_i = values.index(maxv)
    W, H = 900, height
    cy = H / 2
    pad = 16
    slot = (W - 2 * pad) / n
    bw = slot * 0.55
    half = (H / 2) - 22

    bars = ""
    for i, v in enumerate(values):
        x = pad + i * slot + (slot - bw) / 2
        bh = (v / maxv) * half
        is_peak = (i == peak_i)
        c = color if not is_peak else "#2D3748"
        op = "1" if is_peak else "0.75"
        bars += (
            f'<rect x="{x:.1f}" y="{cy - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
            f'rx="2" fill="{c}" opacity="{op}"/>'
            f'<rect x="{x:.1f}" y="{cy:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
            f'rx="2" fill="{c}" opacity="{float(op)*0.55:.2f}"/>'
        )
    # centre line
    line = f'<line x1="{pad}" y1="{cy}" x2="{W-pad}" y2="{cy}" stroke="#CBD5E0" stroke-width="1"/>'
    # peak marker
    px = pad + peak_i * slot + slot / 2
    peak_mark = (
        f'<text x="{px:.1f}" y="{cy - half - 4:.1f}" text-anchor="middle" '
        f'font-size="18">{peak_emoji}</text>'
    )
    # event marker (e.g. product launch / disaster)
    event = ""
    if event_year is not None and event_year in years:
        ei = years.index(event_year)
        ex = pad + ei * slot + slot / 2
        event = (
            f'<line x1="{ex:.1f}" y1="6" x2="{ex:.1f}" y2="{H-18}" stroke="#E63946" '
            f'stroke-width="1.5" stroke-dasharray="4 3" opacity="0.7"/>'
            f'<text x="{ex:.1f}" y="{H-4:.1f}" text-anchor="middle" font-size="10" '
            f'fill="#E63946" font-weight="600">{event_label}</text>'
        )
    # year ticks (first / peak / last)
    ticks = ""
    for i in (0, peak_i, n - 1):
        tx = pad + i * slot + slot / 2
        ticks += (f'<text x="{tx:.1f}" y="14" text-anchor="middle" font-size="10" '
                  f'fill="#A0AEC0">{years[i]}</text>')
    return (
        f'<svg width="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" '
        f'style="display:block;">{line}{bars}{peak_mark}{event}{ticks}</svg>'
    )


def rising_eq(values, years, color, height=200):
    """A rising equalizer / spectrum: each year is a column of stacked level segments,
    brighter toward the top — the 'sound' filling up as the name grows louder."""
    n = len(values); mx = max(values) or 1
    W, H = 900, height; pad = 20; base = H - 26
    bw = (W - 2 * pad) / n * 0.62
    peak_i = values.index(mx)
    svg = f'<svg width="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" style="display:block;">'
    for i, v in enumerate(values):
        x = pad + i * (W - 2 * pad) / n
        h = v / mx * (base - 18)
        segs = max(1, int(h / 9))
        for s in range(segs):
            svg += (f'<rect x="{x:.1f}" y="{base - (s + 1) * 9:.1f}" width="{bw:.1f}" height="7" rx="1.5" '
                    f'fill="{color}" opacity="{0.4 + s / max(segs, 1) * 0.6:.2f}"/>')
    # peak glow dot
    px = pad + peak_i * (W - 2 * pad) / n + bw / 2
    svg += f'<text x="{px:.1f}" y="{base - mx/mx*(base-18) - 8:.1f}" text-anchor="middle" font-size="15">🔊</text>'
    for i in (0, peak_i, n - 1):
        tx = pad + i * (W - 2 * pad) / n + bw / 2
        svg += f'<text x="{tx:.1f}" y="{H-6}" text-anchor="middle" font-size="10" fill="#A0AEC0">{years[i]}</text>'
    return svg + '</svg>'


def rising_eq_card(title, values, years, color, caption):
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:18px 20px;'
        'box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:6px;">'
        f'<div style="font-family:Georgia,serif;font-size:1.3em;font-weight:800;color:#2D3748;margin-bottom:2px;">{title}</div>'
        f'<div style="font-size:.78em;color:#718096;margin-bottom:8px;">{caption}</div>'
        + rising_eq(values, years, color) + '</div>'
    )


def staff(values, years, color, event_year=None, event_label="", crescendo=True, height=200):
    """Notes climbing a musical staff — each year is a note; higher note = louder = more
    popular. A crescendo hairpin underneath swells with the trend. Fully music-themed."""
    n = len(values); maxv = max(values) or 1
    peak_i = values.index(maxv)
    W, H = 900, height
    left, right = 70, W - 24
    s_top, gap = 46, 16           # staff: 5 lines
    s_bot = s_top + gap * 4
    note_lo, note_hi = s_bot + gap, s_top - gap * 2   # value 0 sits below staff, peak floats above
    def X(i): return left + i * (right - left) / (n - 1)
    def Y(v): return note_lo - (v / maxv) * (note_lo - note_hi)
    svg = f'<svg width="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" style="display:block;">'
    # staff lines
    for k in range(5):
        y = s_top + k * gap
        svg += f'<line x1="{left-6}" y1="{y}" x2="{right}" y2="{y}" stroke="#C7CFDD" stroke-width="1.4"/>'
    # treble clef
    svg += f'<text x="18" y="{s_bot+6}" font-size="{gap*5}" fill="{color}" opacity="0.9" font-family="serif">\U0001D11E</text>'
    # connecting slur (light) through the note heads
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(values))
    svg += f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.35"/>'
    # notes
    for i, v in enumerate(values):
        x, y = X(i), Y(v)
        is_peak = (i == peak_i)
        r = 6 if is_peak else 4.5
        stem = "" if is_peak else f'<line x1="{x+r-0.5:.1f}" y1="{y:.1f}" x2="{x+r-0.5:.1f}" y2="{y-22:.1f}" stroke="{color}" stroke-width="1.6"/>'
        glow = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{color}" opacity="0.2"/>' if is_peak else ""
        svg += glow + f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r+1.5:.1f}" ry="{r:.1f}" fill="{color}" transform="rotate(-18 {x:.1f} {y:.1f})"/>' + stem
    # crescendo / decrescendo hairpin under the staff
    hair_y = s_bot + gap * 2.2
    if crescendo:
        svg += (f'<line x1="{left}" y1="{hair_y}" x2="{right-40}" y2="{hair_y-9}" stroke="{color}" stroke-width="2"/>'
                f'<line x1="{left}" y1="{hair_y}" x2="{right-40}" y2="{hair_y+9}" stroke="{color}" stroke-width="2"/>'
                f'<text x="{left-4}" y="{hair_y+22}" font-size="12" fill="#718096" font-style="italic">pp</text>'
                f'<text x="{right-34}" y="{hair_y+4}" font-size="13" fill="{color}" font-style="italic" font-weight="700">ƒƒ crescendo</text>')
    # event marker
    if event_year is not None and event_year in years:
        ex = X(years.index(event_year))
        svg += (f'<line x1="{ex:.1f}" y1="{s_top-14}" x2="{ex:.1f}" y2="{s_bot+8}" stroke="#E63946" '
                f'stroke-width="1.5" stroke-dasharray="4 3" opacity="0.7"/>'
                f'<text x="{ex:.1f}" y="{s_top-18}" text-anchor="middle" font-size="10" fill="#E63946" font-weight="600">{event_label}</text>')
    # year ticks
    for i in (0, peak_i, n - 1):
        svg += f'<text x="{X(i):.1f}" y="{H-6}" text-anchor="middle" font-size="10" fill="#A0AEC0">{years[i]}</text>'
    return svg + '</svg>'


def staff_card(title, values, years, color, event_year, event_label, caption, crescendo=True):
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:18px 20px;'
        'box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:6px;">'
        f'<div style="font-family:Georgia,serif;font-size:1.3em;font-weight:800;color:#2D3748;margin-bottom:2px;">{title}</div>'
        f'<div style="font-size:.78em;color:#718096;margin-bottom:6px;">{caption}</div>'
        + staff(values, years, color, event_year, event_label, crescendo) + '</div>'
    )


def ridge(values, years, color, event_year=None, event_label="", height=150):
    """A smooth filled area 'ridge' (single-direction, not mirrored bars) — clean
    upward or rise/fall silhouette with a glowing peak dot."""
    n = len(values); maxv = max(values) or 1
    peak_i = values.index(maxv)
    W, H = 900, height; pad = 16; base = H - 22; top = 14
    def X(i): return pad + i * (W - 2 * pad) / (n - 1)
    def Y(v): return base - (v / maxv) * (base - top)
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(values))
    area = f"{pad},{base} {pts} {W-pad},{base}"
    peak_dot = f'<circle cx="{X(peak_i):.1f}" cy="{Y(maxv):.1f}" r="5" fill="{color}"/>' \
               f'<circle cx="{X(peak_i):.1f}" cy="{Y(maxv):.1f}" r="9" fill="{color}" opacity="0.25"/>'
    event = ""
    if event_year is not None and event_year in years:
        ex = X(years.index(event_year))
        event = (f'<line x1="{ex:.1f}" y1="6" x2="{ex:.1f}" y2="{base}" stroke="#E63946" '
                 f'stroke-width="1.5" stroke-dasharray="4 3" opacity="0.7"/>'
                 f'<text x="{ex:.1f}" y="{H-4:.1f}" text-anchor="middle" font-size="10" '
                 f'fill="#E63946" font-weight="600">{event_label}</text>')
    ticks = ""
    for i in (0, peak_i, n - 1):
        ticks += (f'<text x="{X(i):.1f}" y="12" text-anchor="middle" font-size="10" '
                  f'fill="#A0AEC0">{years[i]}</text>')
    return (
        f'<svg width="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="none" style="display:block;">'
        f'<polygon points="{area}" fill="{color}" opacity="0.16"/>'
        f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3" '
        f'stroke-linejoin="round" stroke-linecap="round"/>{peak_dot}{event}{ticks}</svg>'
    )


def ridge_card(title, values, years, color, event_year, event_label, caption):
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:18px 20px;'
        'box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:6px;">'
        f'<div style="font-family:Georgia,serif;font-size:1.3em;font-weight:800;color:#2D3748;margin-bottom:2px;">{title}</div>'
        f'<div style="font-size:.78em;color:#718096;margin-bottom:10px;">{caption}</div>'
        + ridge(values, years, color, event_year, event_label) + '</div>'
    )


def wave_card(title, values, years, color, peak_emoji, event_year, event_label, caption):
    """A framed soundwave with a title + caption."""
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:18px 20px;'
        'box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:6px;">'
        f'<div style="font-family:Georgia,serif;font-size:1.3em;font-weight:800;color:#2D3748;'
        f'margin-bottom:2px;">{title}</div>'
        f'<div style="font-size:.78em;color:#718096;margin-bottom:10px;">{caption}</div>'
        + soundwave(values, years, color, peak_emoji, 150, event_year, event_label) +
        '</div>'
    )


def multitrack(rows, unit="peak"):
    """Each name = a mixing-desk track: label + inline mini-waveform + peak readout."""
    html = ('<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
            'border:1px solid #E2E8F0;border-radius:16px;padding:16px 18px;'
            'box-shadow:0 4px 16px rgba(0,0,0,.06);">')
    for name, sub, values, years, color in rows:
        peak = max(values)
        peak_yr = years[values.index(peak)]
        html += (
            '<div style="display:grid;grid-template-columns:150px 1fr 90px;align-items:center;'
            'gap:14px;padding:8px 0;border-bottom:1px solid rgba(226,232,240,0.7);">'
            f'<div><div style="font-weight:800;color:#2D3748;font-size:1.05em;">{name}</div>'
            f'<div style="font-size:.7em;color:#718096;line-height:1.25;">{sub}</div></div>'
            f'<div>{soundwave(values, years, color, "▲", 64)}</div>'
            f'<div style="text-align:right;"><div style="font-weight:800;color:{color};font-size:1.15em;">{peak:,}</div>'
            f'<div style="font-size:.66em;color:#A0AEC0;">{unit} · {peak_yr}</div></div>'
            '</div>'
        )
    html += '</div>'
    return html


def revival_panel(rows):
    """All comeback names in ONE panel — each a row with a waveform that flatlines
    then erupts, a ×N badge, and trough→peak markers. rows: (name, sub, values, years, color, ratio)."""
    inner = ""
    for i, (name, sub, values, years, color, ratio) in enumerate(rows):
        trough = min(values); trough_yr = years[values.index(trough)]
        peak = max(values); peak_yr = years[values.index(peak)]
        border = "" if i == 0 else "border-top:1px solid rgba(226,232,240,0.9);padding-top:16px;"
        inner += (
            f'<div style="{border}margin-bottom:16px;">'
            '<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px;">'
            f'<div><span style="font-family:Georgia,serif;font-size:1.4em;font-weight:800;color:#2D3748;">{name}</span>'
            f'<span style="font-size:.78em;color:#718096;margin-left:10px;">{sub}</span></div>'
            f'<div style="background:{color};color:#fff;font-weight:800;font-size:.9em;'
            f'padding:3px 14px;border-radius:20px;">▲ {ratio} revival</div>'
            '</div>'
            + soundwave(values, years, color, "📈", 96) +
            '<div style="display:flex;justify-content:space-between;font-size:.72em;color:#718096;">'
            f'<span>💀 flatlined at <b>{trough}</b> ({trough_yr})</span>'
            f'<span>🔥 back to <b>{peak:,}</b> ({peak_yr})</span>'
            '</div></div>'
        )
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:20px 24px;'
        'box-shadow:0 4px 16px rgba(0,0,0,.06);">' + inner + '</div>'
    )


def cassette_pair(name, peak_val, peak_yr, now_val, now_yr, event, color):
    """A cassette tape being ERASED: 'before' has full reels, 'after' is demagnetised/empty.
    Perfect for the corporate-erasure story."""
    def tape(label, val, yr, spool, dim, c):
        op = "0.35" if dim else "1"
        # two reels; 'spool' 0..1 = how full the tape still is
        r_full = 6 + spool * 12
        return (
            '<div style="flex:1;min-width:230px;background:linear-gradient(160deg,#2A2438,#161226);'
            'border-radius:14px;padding:20px;text-align:center;box-shadow:0 10px 26px rgba(0,0,0,.3);">'
            f'<div style="font-size:.6rem;letter-spacing:2px;font-weight:800;color:{c};">{label}</div>'
            f'<svg width="180" height="110" viewBox="0 0 180 110" style="margin:12px auto 4px;opacity:{op};">'
            '<rect x="6" y="6" width="168" height="98" rx="10" fill="#12101c" stroke="#3a3350" stroke-width="1.5"/>'
            '<rect x="26" y="30" width="128" height="40" rx="6" fill="#1c1830" stroke="#3a3350"/>'
            # reels
            f'<circle cx="60" cy="50" r="22" fill="none" stroke="#3a3350" stroke-width="2"/>'
            f'<circle cx="60" cy="50" r="{r_full:.0f}" fill="{c}" opacity="0.9"/>'
            f'<circle cx="60" cy="50" r="4" fill="#12101c"/>'
            f'<circle cx="120" cy="50" r="22" fill="none" stroke="#3a3350" stroke-width="2"/>'
            f'<circle cx="120" cy="50" r="{(1-spool)*12+6:.0f}" fill="{c}" opacity="0.9"/>'
            f'<circle cx="120" cy="50" r="4" fill="#12101c"/>'
            '<rect x="40" y="84" width="100" height="10" rx="3" fill="#1c1830"/>'
            '</svg>'
            f'<div style="font-size:2em;font-weight:800;color:{c};">{val}</div>'
            f'<div style="font-size:.72em;color:#9A8FB0;">babies/yr · {yr}</div>'
            '</div>'
        )
    return (
        f'<div style="font-weight:700;color:#2D3748;margin-bottom:6px;">🎙️ {name} — {event}</div>'
        '<div style="display:flex;gap:16px;flex-wrap:wrap;">'
        + tape("● RECORDED · PEAK", peak_val, peak_yr, 1.0, False, color)
        + tape("● ERASED · TODAY", now_val, now_yr, 0.05, True, "#E63946")
        + '</div>'
    )


def volume_dial(value, maxv, color, from_label, to_label, event):
    """An amp gain knob turned up from silence — for a name going 0 → loud."""
    import math
    frac = min(value / maxv, 1.0)
    ang = -135 + frac * 270            # -135° (min) .. +135° (max)
    rad = math.radians(ang)
    cx, cy, r = 90, 90, 60
    px = cx + r * 0.7 * math.sin(rad)
    py = cy - r * 0.7 * math.cos(rad)
    # tick marks around the dial
    ticks = ""
    for t in range(11):
        a = math.radians(-135 + t * 27)
        x1 = cx + r * 0.92 * math.sin(a); y1 = cy - r * 0.92 * math.cos(a)
        x2 = cx + r * 1.05 * math.sin(a); y2 = cy - r * 1.05 * math.cos(a)
        lit = (t / 10) <= frac
        ticks += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                  f'stroke="{color if lit else "#3a3350"}" stroke-width="3" stroke-linecap="round"/>')
    return (
        '<div style="background:linear-gradient(160deg,#2A2438,#161226);border-radius:16px;'
        'padding:22px;text-align:center;box-shadow:0 8px 22px rgba(0,0,0,.3);">'
        f'<div style="font-size:.62rem;letter-spacing:2px;color:{color};font-weight:800;margin-bottom:6px;">🔊 VOLUME · from silence to loud</div>'
        f'<svg width="180" height="150" viewBox="0 0 180 150" style="margin:0 auto;">'
        + ticks +
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#12101c" stroke="{color}" stroke-width="2"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="6" fill="{color}"/>'
        f'<text x="{cx-r}" y="148" font-size="10" fill="#9A8FB0">{from_label}</text>'
        f'<text x="{cx+r-20}" y="148" font-size="10" fill="{color}" font-weight="700">{to_label}</text>'
        '</svg>'
        f'<div style="font-size:.75em;color:#9A8FB0;margin-top:4px;">{event}</div>'
        '</div>'
    )


def chart_countdown(rows):
    """A radio 'Top of the Charts' countdown — ranked rows, each name climbing with an arrow.
    rows: (name, sub, peak, peak_yr, color). Ranked by peak descending."""
    rows = sorted(rows, key=lambda r: -r[2])
    items = ""
    for i, (name, sub, peak, peak_yr, color) in enumerate(rows):
        rank = i + 1
        items += (
            '<div style="display:flex;align-items:center;gap:16px;padding:11px 16px;margin:7px 0;'
            'background:#fff;border:1px solid #eee;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.04);">'
            f'<div style="font-size:1.4em;font-weight:800;color:{color};min-width:36px;text-align:center;">#{rank}</div>'
            f'<div style="flex:1;"><div style="font-weight:800;color:#2D3748;font-size:1.05em;">{name} '
            f'<span style="color:{color};font-size:.8em;">▲ climbing</span></div>'
            f'<div style="font-size:.72em;color:#718096;">{sub}</div></div>'
            f'<div style="text-align:right;"><div style="font-weight:800;color:{color};font-size:1.15em;">{peak:,}</div>'
            f'<div style="font-size:.66em;color:#A0AEC0;">peak · {peak_yr}</div></div>'
            '</div>'
        )
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);border:1px solid #E2E8F0;'
        'border-radius:16px;padding:16px 18px;box-shadow:0 4px 16px rgba(0,0,0,.06);">'
        '<div style="text-align:center;font-size:.72em;letter-spacing:2px;color:#718096;'
        'text-transform:uppercase;font-weight:700;margin-bottom:10px;">📻 TOP OF THE CHARTS · once-forbidden names</div>'
        + items + '</div>'
    )


def vinyl_pair(left, right):
    """Two spinning-record cards side by side — a 'before / after' 45rpm single.
    Each: (label, name, sub, big_value, small, color, spun_out)."""
    def disc(label, name, sub, big, small, color, dim=False):
        op = "0.4" if dim else "1"
        return (
            '<div style="flex:1;min-width:220px;background:linear-gradient(160deg,#2A2438,#1A1626);'
            'border-radius:16px;padding:24px;text-align:center;box-shadow:0 10px 28px rgba(0,0,0,.3);">'
            f'<div style="font-size:.6rem;letter-spacing:3px;font-weight:800;color:{color};">{label}</div>'
            f'<svg width="120" height="120" viewBox="0 0 100 100" style="margin:14px auto 6px;opacity:{op};">'
            '<circle cx="50" cy="50" r="48" fill="#12101c"/>'
            '<circle cx="50" cy="50" r="34" fill="none" stroke="#3a3350" stroke-width="1.2"/>'
            '<circle cx="50" cy="50" r="24" fill="none" stroke="#3a3350" stroke-width="1.2"/>'
            f'<circle cx="50" cy="50" r="15" fill="{color}"/><circle cx="50" cy="50" r="4" fill="#12101c"/></svg>'
            f'<div style="font-family:Georgia,serif;font-size:1.5em;font-weight:800;color:#F0EBFA;">{name}</div>'
            f'<div style="font-size:.72em;color:#9A8FB0;margin-bottom:8px;">{sub}</div>'
            f'<div style="font-size:2em;font-weight:800;color:{color};">{big}</div>'
            f'<div style="font-size:.72em;color:#A0AEC0;">{small}</div>'
            '</div>'
        )
    return ('<div style="display:flex;gap:18px;flex-wrap:wrap;">'
            + disc(*left) + disc(*right) + '</div>')


def equalizer(rows, title):
    """A vertical EQ: each item is a column of stacked 'level' segments (like a graphic
    equalizer / VU meter). rows: (label, value, max_value, color)."""
    cols = ""
    for label, val, mx, color in rows:
        lit = round(val / mx * 10)
        segs = ""
        for s in range(10, 0, -1):
            on = s <= lit
            segs += (f'<div style="width:26px;height:9px;border-radius:2px;margin:2px 0;'
                     f'background:{color if on else "#E2E8F0"};opacity:{"1" if on else "0.6"};"></div>')
        cols += (
            '<div style="text-align:center;">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">{segs}</div>'
            f'<div style="font-weight:800;color:{color};font-size:1.05em;margin-top:8px;">{val:,}</div>'
            f'<div style="font-size:.72em;color:#4A5568;font-weight:600;">{label}</div>'
            '</div>'
        )
    return (
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:24px 20px;box-shadow:0 4px 16px rgba(0,0,0,.06);">'
        f'<div style="text-align:center;font-size:.72em;letter-spacing:2px;color:#718096;'
        f'text-transform:uppercase;font-weight:700;margin-bottom:18px;">{title}</div>'
        '<div style="display:flex;justify-content:center;gap:30px;align-items:flex-end;flex-wrap:wrap;">'
        + cols + '</div></div>'
    )


def climb_cards(cards):
    """Rising 'ascending stairs' cards — each riser shown as an upward arrow-ramp
    with from → to values. cards: (name, meaning, from_v, to_v, color)."""
    tiles = ""
    for name, meaning, fromv, tov, color in cards:
        # small ascending ramp of 5 blocks
        ramp = "".join(
            f'<div style="width:9px;height:{8 + i*7}px;background:{color};'
            f'border-radius:2px;opacity:{0.5 + i*0.12:.2f};"></div>' for i in range(5)
        )
        tiles += (
            '<div style="flex:1;min-width:150px;background:#fff;border:1px solid #E2E8F0;'
            'border-radius:14px;padding:18px 16px;box-shadow:0 4px 12px rgba(0,0,0,.05);">'
            f'<div style="font-family:Georgia,serif;font-size:1.4em;font-weight:800;color:#2D3748;">{name}</div>'
            f'<div style="font-size:.72em;color:#718096;font-style:italic;margin-bottom:12px;">{meaning}</div>'
            f'<div style="display:flex;align-items:flex-end;gap:4px;height:44px;">{ramp}'
            f'<span style="margin-left:6px;color:{color};font-size:1.3em;">↗</span></div>'
            f'<div style="margin-top:12px;font-size:.9em;color:#4A5568;">'
            f'<b style="color:#A0AEC0;">{fromv}</b> <span style="color:#CBD5E0;">→</span> '
            f'<b style="color:{color};font-size:1.15em;">{tov:,}</b></div>'
            '<div style="font-size:.66em;color:#A0AEC0;">babies/yr · 1997 → 2023</div>'
            '</div>'
        )
    return '<div style="display:flex;gap:14px;flex-wrap:wrap;">' + tiles + '</div>'


def poster_wall(cards):
    """Movie-marquee 'now showing' posters — for names invented by fiction.
    cards: (name, source, year, from_zero_to, color)."""
    tiles = ""
    for name, source, year, arc, color in cards:
        tiles += (
            f'<div style="flex:1;min-width:150px;background:linear-gradient(180deg,#1A1A2E,#16213E);'
            f'border-radius:10px;padding:18px 14px;text-align:center;border-top:4px solid {color};'
            f'box-shadow:0 8px 20px rgba(0,0,0,.3);">'
            '<div style="font-size:.55rem;letter-spacing:2px;color:#ECC94B;font-weight:700;">🎬 NOW SHOWING</div>'
            f'<div style="font-family:Georgia,serif;font-size:1.5em;font-weight:800;color:#F0EBFA;margin:10px 0 2px;">{name}</div>'
            f'<div style="font-size:.72em;color:#9FB0C8;font-style:italic;">{source}</div>'
            f'<div style="margin:12px 0 4px;font-size:.7rem;color:#718096;">premiered {year}</div>'
            f'<div style="font-size:1.05em;font-weight:800;color:{color};">{arc}</div>'
            '</div>'
        )
    return '<div style="display:flex;gap:14px;flex-wrap:wrap;">' + tiles + '</div>'


def render():
    _years = list(range(1997, 2024))

    # ─── Header ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4);
                    border-radius: 16px; padding: 50px 30px; text-align: center;
                    margin-bottom: 20px; border: 1px solid #E2E8F0;">
            <h1 style="font-size: 2.8em; font-weight: 800; color: #2D3748; margin: 0 0 12px 0;">
                🎉 I Never Knew That
            </h1>
            <p style="font-size: 1.2em; color: #4A5568; max-width: 650px; margin: 0 auto; line-height: 1.7;">
                Five surprising stories hiding in 27 years of baby name data —
                told the way they deserve: on record, on the charts, on the marquee.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════
    # 🤖 CORPORATE ERASURE
    # ══════════════════════════════════════════════════════════════
    st.markdown("### 🤖 Corporate Erasure")
    st.markdown("What happens when a tech giant names a product after a human name? The humans stop using it.")

    # Cassette tapes being erased — full reels (peak) → demagnetised/empty (today)
    st.markdown(cassette_pair("Alexa", "6,702", "2015", "511", "2023",
        "the chart-topper wiped by Amazon Echo (2014) · −92%", "#7C9FD6"), unsafe_allow_html=True)
    st.markdown("")
    st.markdown(cassette_pair("Siri", "94", "2010", "7", "2023",
        "a rising star cut off mid-climb by Apple Siri (2011) · −93%", "#C8A8E8"), unsafe_allow_html=True)
    st.markdown("")
    st.info(
        "💡 **The asymmetry:** Alexa had a bigger victim pool (6,702/year) but Siri was the crueller kill "
        "— it was actively *growing* when Apple took it. Alexa was already past peak."
    )
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 🧟 BACK FROM THE DEAD (Zombie Names) — multitrack
    # ══════════════════════════════════════════════════════════════
    st.markdown("### 🧟 Back from the Dead")
    st.markdown(
        "Some names flatline completely — years of single digits, near-zero. Then something happens: "
        "a TV show, a cultural shift, a vibe change. And the name claws its way back. "
        "Each track below is the name's own comeback clip:"
    )
    zombie_rows = [
        ("Wren", "cottagecore + nature names", [3,6,5,14,11,17,24,54,41,86,107,159,203,288,419,504,569,855,1012,1053,1159,1325,1988,2596,2535], list(range(1999,2024)), "#48BB78", "865×"),
        ("Salem", "WitchTok + Sabrina (2018)", [34,18,40,9,44,43,40,43,55,46,54,56,70,77,57,84,88,150,220,263,305,327,564,711,951,1152,1246], _years, "#9B6FD4", "138×"),
        ("Octavia", "The 100 — Octavia Blake", [220,233,202,177,156,176,128,74,143,84,67,91,79,47,43,63,53,66,279,391,682,943,1066,1152,1577,1509,1441], _years, "#F56565", "37×"),
        ("Xena", "streaming revival", [246,156,86,74,37,31,18,10,13,13,14,12,13,18,14,34,38,38,58,70,109,126,162,169,162,278,261], _years, "#7C9FD6", "28×"),
    ]
    st.markdown(revival_panel(zombie_rows), unsafe_allow_html=True)
    st.markdown(
        "**What brings a name back?** Streaming reviving old shows (Xena), a breakout character (Octavia), "
        "or aesthetic movements going viral (Salem, Wren). Watch each waveform: silent for years, then it *erupts*."
    )
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 🕉️ IMMIGRATION WRITTEN IN NAMES — soundwave + risers multitrack
    # ══════════════════════════════════════════════════════════════
    st.markdown("### 🕉️ Immigration Written in Names")
    st.markdown(
        "The Indian diaspora is large enough to register simultaneously in all 8 countries. "
        "Sanskrit-rooted names surged across the Anglosphere this generation — a rising chord, not a fall:"
    )
    indian_totals = [3814,4742,8167,7049,7626,7939,8321,9260,10366,10853,11960,12643,12549,13199,14990,18017,21308,24106,25156,27432,28523,29007,29177,26783,27775,28822,28607]
    st.markdown(rising_eq_card("Sanskrit / Indian names — combined", indian_totals, _years, "#F6AD55",
        "3,814 (1997) → 28,607 (2023) · +650% — the sound filling up across the Anglosphere"),
        unsafe_allow_html=True)

    st.markdown("**Top individual risers — each climbed from near-silence:**")
    st.markdown(climb_cards([
        ("Aria", "Sanskrit 'melody' / air", "93", 8819, "#F6AD55"),
        ("Arya", "'noble'", "24", 2691, "#F5A9C0"),
        ("Ayaan", "'gift of God'", "4", 1163, "#9B6FD4"),
        ("Aarav", "'peaceful'", "0", 718, "#48BB78"),
        ("Ishaan", "'the sun'", "0", 398, "#7C9FD6"),
    ]), unsafe_allow_html=True)
    st.info(
        "💡 These names have LOW countryness (2–4) — shared equally across diaspora countries. "
        "Indian families name children the same way regardless of which country they're in — "
        "a global culture writing itself into eight national songbooks at once."
    )
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 🎛️ THE 'J' COLLAPSE — mixing board faders (kept)
    # ══════════════════════════════════════════════════════════════
    st.markdown("### 🎛️ The Great 'J' Collapse")
    st.markdown(
        "Every letter has its era. The 'J' names that defined the '90s — Jessica, Jason, Jennifer, Jacob — "
        "are quietly vanishing. On the naming mixing board, each initial slid up or down since 1997:"
    )
    letter_change = [
        ("J", -6.01, "#E63946"), ("C", -2.65, "#F56565"), ("D", -2.26, "#F6AD55"),
        ("A", 1.74, "#7C9FD6"), ("E", 3.26, "#68B58A"), ("L", 3.65, "#48BB78"),
    ]
    max_abs = max(abs(v) for _, v, _ in letter_change)
    faders = ""
    for letter, val, color in letter_change:
        rising = val >= 0
        fill_h = int(abs(val) / max_abs * 70)
        knob_bottom = 78 + fill_h if rising else 78 - fill_h
        arrow = "▲" if rising else "▼"
        faders += (
            '<div style="text-align:center;">'
            '<div style="position:relative;width:34px;height:160px;margin:0 auto;'
            'background:linear-gradient(#E2E8F0,#EDF2F7);border-radius:8px;border:1px solid #DDE3EC;">'
            '<div style="position:absolute;top:78px;left:0;right:0;height:2px;background:#CBD5E0;"></div>'
            + (f'<div style="position:absolute;left:9px;width:14px;bottom:82px;height:{fill_h}px;'
               f'background:{color};border-radius:6px 6px 0 0;"></div>' if rising else
               f'<div style="position:absolute;left:9px;width:14px;top:78px;height:{fill_h}px;'
               f'background:{color};border-radius:0 0 6px 6px;"></div>')
            + f'<div style="position:absolute;left:4px;width:26px;height:12px;bottom:{knob_bottom-6}px;'
              f'background:#fff;border:2px solid {color};border-radius:4px;box-shadow:0 2px 5px rgba(0,0,0,.15);"></div>'
            '</div>'
            f'<div style="font-family:Georgia,serif;font-size:1.6em;font-weight:800;color:{color};margin-top:8px;">{letter}</div>'
            f'<div style="font-size:.8em;font-weight:700;color:{color};">{arrow} {val:+.1f}</div>'
            '</div>'
        )
    st.markdown(
        '<div style="background:linear-gradient(135deg,#EEF2FF,#E8F4FD,#F0FFF4);'
        'border:1px solid #E2E8F0;border-radius:16px;padding:24px 20px;box-shadow:0 4px 16px rgba(0,0,0,.06);">'
        '<div style="text-align:center;font-size:.72em;letter-spacing:2px;color:#718096;'
        'text-transform:uppercase;font-weight:700;margin-bottom:16px;">🎛️ THE NAMING MIXING BOARD · first-letter share, 1997 → 2023</div>'
        '<div style="display:flex;justify-content:center;gap:22px;flex-wrap:wrap;">' + faders + '</div>'
        '<div style="display:flex;justify-content:space-between;max-width:520px;margin:14px auto 0;">'
        '<span style="font-size:.72em;color:#48BB78;font-weight:700;">▲ FADED UP</span>'
        '<span style="font-size:.72em;color:#E63946;font-weight:700;">FADED DOWN ▼</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "**'J' lost 6 percentage points** — a bigger drop than any other letter. Meanwhile soft-sounding "
        "**'L'** (Liam, Luca, Lily) and **'E'** (Emma, Ella, Ethan) names gained the most."
    )
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 😈 THE TABOO THAT BROKE — soundwave + two multitracks
    # ══════════════════════════════════════════════════════════════
    st.markdown("### 😈 The Taboo That Broke")
    st.markdown(
        "Some names sit behind an invisible line no one crosses — until pop culture quietly moves the line. "
        "**Zero** babies were named Lucifer for years… then a hit show rebranded the devil as a charming lead."
    )
    col_luc, col_note = st.columns([1, 1])
    with col_luc:
        st.markdown(volume_dial(77, 77, "#9B6FD4", "0 · silent", "77 · 2022",
            "Netflix's Lucifer (2016) cranked the name from mute to loud"), unsafe_allow_html=True)
    with col_note:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F5F0FF, #EDE9FE); border-radius: 12px;
                    padding: 24px; border: 1px solid #E2D9F3; height: 100%;
                    display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 1px;">Before 2016</div>
            <div style="font-size: 2.4em; font-weight: 800; color: #9B6FD4;">0</div>
            <div style="font-size: 0.85em; color: #4A5568; margin-bottom: 14px;">the name no one dared</div>
            <div style="font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 1px;">Peak (2022)</div>
            <div style="font-size: 2.4em; font-weight: 800; color: #6B46C1;">77</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 👑 Naming a Baby a Title")
    st.markdown(
        "You couldn't once call a child *King* or *Messiah* — it was arrogant, even blasphemous. "
        "Today thousands do. Each track shows the taboo lifting:"
    )
    st.markdown(chart_countdown([
        ("Legend", "pure aspiration", 3191, 2021, "#48BB78"),
        ("King", "a title, not a name", 2778, 2017, "#ECC94B"),
        ("Messiah", "once blasphemous", 2226, 2021, "#9B6FD4"),
        ("Saint", "reverent → mainstream", 1216, 2023, "#7C9FD6"),
    ]), unsafe_allow_html=True)

    st.markdown("#### 🎬 Straight Out of Fiction")
    st.markdown(
        "Some names didn't exist at all until a screen invented them — flat silence, then a spike the "
        "moment the show or film lands. Names with **no history before their premiere:**"
    )
    st.markdown(poster_wall([
        ("Kylo", "Star Wars", 2015, "0 → 1,042", "#7C9FD6"),
        ("Khaleesi", "Game of Thrones", 2011, "0 → 606", "#48BB78"),
        ("Renesmee", "Twilight", 2008, "0 → 206", "#F56565"),
        ("Draco", "Harry Potter", 2001, "0 → 143", "#ECC94B"),
    ]), unsafe_allow_html=True)
    st.markdown(
        "**Khaleesi** (*Game of Thrones*, 2011) went 0 → 606. **Kylo** (*Star Wars*, 2015) exploded to over "
        "1,000 a year. Each name literally did not exist until fiction spoke it into being."
    )
    st.markdown("---")

    # ─── Closing note ─────────────────────────────────────────────
    st.markdown(
        "<div style='text-align:center; color:#718096; font-style:italic; padding: 10px 0 30px;'>"
        "Every one of these was hiding in the same 200 million names — you just had to know where to listen. 🎧"
        "</div>",
        unsafe_allow_html=True,
    )
