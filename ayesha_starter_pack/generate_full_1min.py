#!/usr/bin/env python3
"""~1 minute hyperpop beat @ 138 BPM (35 bars) — drums + 808, F#maj."""

from pathlib import Path

from midiutil import MIDIFile

BPM = 138
BARS = 35  # 35 * 4 = 140 beats ≈ 60.9 sec
OUT = Path(__file__).resolve().parent

KICK, SNARE, CHH, OHH, CLAP, RIM, CRASH = 36, 38, 42, 46, 39, 37, 49


def section(bar: int) -> str:
    if bar < 4:
        return "intro"
    if bar < 12:
        return "verse1"
    if bar < 16:
        return "build"
    if bar < 24:
        return "hook"
    if bar < 28:
        return "verse2"
    if bar < 32:
        return "break"
    return "outro"


def add_kicks(mf, base: float, bar: int, sec: str) -> None:
    patterns = {
        "intro": [0, 2],
        "verse1": [0, 0.75, 1.75, 2.5, 3.25],
        "build": [0, 0.5, 1.5, 2, 2.75, 3.25, 3.5],
        "hook": [0, 0.75, 1.5, 1.75, 2.5, 3, 3.25],
        "verse2": [0, 1.25, 2, 2.5, 3.5],
        "break": [0, 2],
        "outro": [0, 0.75, 1.5, 2.5, 3, 3.25, 3.5, 3.75],
    }
    for b in patterns[sec]:
        vel = 115 if b == 0 and sec in ("hook", "build") else 100
        if sec == "intro":
            vel = 75
        mf.addNote(0, 9, KICK, base + b, 0.14, vel)


def add_snare_clap(mf, base: float, sec: str, bar: int) -> None:
    if sec == "intro":
        if bar == 3:
            mf.addNote(0, 9, SNARE, base + 2, 0.1, 70)
        return
    if sec == "break":
        mf.addNote(0, 9, SNARE, base + 2, 0.08, 65)
        return
    mf.addNote(0, 9, SNARE, base + 2, 0.11, 108 if sec == "hook" else 100)
    mf.addNote(0, 9, CLAP, base + 2.03, 0.09, 95 if sec == "hook" else 88)
    ghosts = []
    if sec in ("hook", "build"):
        ghosts = [1.5, 3.5]
    elif sec == "verse2":
        ghosts = [3.5]
    for g in ghosts:
        mf.addNote(0, 9, SNARE, base + g, 0.06, 72)


def add_hats(mf, base: float, sec: str, bar: int) -> None:
    if sec == "break" and bar < 30:
        for i in range(8):
            beat = base + i * 0.5
            mf.addNote(0, 9, CHH, beat, 0.05, 55)
        return
    for i in range(16):
        beat = base + i * 0.25
        # fills
        if sec == "build" and bar == 15 and i >= 12:
            mf.addNote(0, 9, CHH, beat, 0.04, 50 + (i - 12) * 14)
            if i < 15:
                mf.addNote(0, 9, CHH, beat + 0.125, 0.03, 70)
            continue
        if sec == "outro" and i >= 13:
            mf.addNote(0, 9, CHH, beat, 0.035, 45 + i * 3)
            continue
        if sec == "hook" and bar in (19, 23) and i >= 14:
            mf.addNote(0, 9, CHH, beat, 0.04, 80)
            continue
        vel = 105 if i % 4 == 0 else (82 if i % 2 == 0 else 58)
        if sec == "intro":
            vel = int(vel * 0.65)
        note = OHH if i in (6, 14) and sec in ("hook", "build", "verse1") else CHH
        mf.addNote(0, 9, note, beat, 0.055, vel)


def add_rim_crash(mf, base: float, sec: str, bar: int) -> None:
    if sec in ("verse1", "verse2", "hook") and bar % 2 == 1:
        mf.addNote(0, 9, RIM, base + 1, 0.05, 78)
        mf.addNote(0, 9, RIM, base + 3, 0.05, 75)
    if bar == 16:
        mf.addNote(0, 9, CRASH, base, 0.4, 90)
    if bar == 24 and sec == "hook":
        mf.addNote(0, 9, CRASH, base, 0.25, 85)


def write_drums(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Ayesha full 1min drums")
    for bar in range(BARS):
        base = bar * 4
        sec = section(bar)
        add_kicks(mf, base, bar, sec)
        add_snare_clap(mf, base, sec, bar)
        add_hats(mf, base, sec, bar)
        add_rim_crash(mf, base, sec, bar)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_bass(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "808 full 1min F#")
    # F#2=42 C#3=49 D#3=51 B2=47 G#2=44
    roots_map = {
        "intro": [42],
        "verse1": [42, 42, 49, 47],
        "build": [42, 49, 51, 47],
        "hook": [42, 44, 49, 47],
        "verse2": [42, 51, 49, 42],
        "break": [42],
        "outro": [42, 47, 49, 42],
    }
    for bar in range(BARS):
        base = bar * 4
        sec = section(bar)
        roots = roots_map[sec]
        root = roots[bar % len(roots)]
        dur = 3.8 if sec in ("verse1", "hook", "verse2") else 2.5
        vel = 110 if sec == "hook" else (85 if sec == "intro" else 100)
        if sec == "break":
            vel = 70
            dur = 3.9
        mf.addNote(0, 0, root, base, dur, vel)
        if sec in ("hook", "build", "verse2") and bar % 2 == 0:
            mf.addNote(0, 0, root, base + 2.5, 0.28, 88)
        if sec == "hook" and bar % 4 == 3:
            mf.addNote(0, 0, root + 12, base + 3.2, 0.25, 82)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_arrangement_txt(path: Path) -> None:
    text = f"""БИТ ~1 МИНУТА | {BPM} BPM | {BARS} тактов | ~61 сек

СТРУКТУРА (куда читать):
  0:00–0:07  INTRO (такты 1–4)     — вступление, можно ad-lib
  0:07–0:21  VERSE 1 (5–12)        — основной куплет (~16 строк)
  0:21–0:28  BUILD (13–16)         — нарастание перед припевом
  0:28–0:42  HOOK (17–24)          — припев, самая плотная часть
  0:42–0:49  VERSE 2 (25–28)       — второй куплет (вариация бита)
  0:49–0:56  BREAK (29–32)         — полупауза, акцент на голос
  0:56–1:01  OUTRO (33–35)         — финал, можно затихание

ФАЙЛЫ:
  beat_full_1min_drums.mid  → Drum Rack
  beat_full_1min_808.mid    → Operator / 808

Тональность: F# (под луп PLX_MTP_138_F#maj)
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    write_drums(OUT / "beat_full_1min_drums.mid")
    write_bass(OUT / "beat_full_1min_808.mid")
    write_arrangement_txt(OUT / "BEAT_1MIN_ARRANGEMENT.txt")
    print(f"Done: {BARS} bars @ {BPM} BPM (~{BARS * 4 / BPM * 60:.0f}s)")


if __name__ == "__main__":
    main()
