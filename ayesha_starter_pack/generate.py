#!/usr/bin/env python3
"""Hyperpop starter MIDI — F# major, 138 BPM."""

from pathlib import Path

from midiutil import MIDIFile

BPM = 138
BARS = 8
OUT = Path(__file__).resolve().parent

KICK, SNARE, CHH, OHH, CLAP, RIM = 36, 38, 42, 46, 39, 37

Fsh, Gsh, Ash, B, Csh, Dsh = 66, 68, 70, 71, 73, 75
Fsh_maj = [Fsh, Ash, Csh]
B_maj = [B, Dsh, 78]
Csh_maj = [Csh, 77, 80]
Dsh_min = [Dsh, 78, 82]
Gsh_min = [Gsh, 71, 75]


def total_beats():
    return BARS * 4


def write_beat_ayesha_short(path: Path, bars: int = 4) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Ayesha beat 4 bars")
    for bar in range(bars):
        base = bar * 4
        kicks = [0, 0.75, 1.75, 2.5, 3.25] if bar % 2 == 0 else [0, 1.5, 2.5, 3.0]
        for b in kicks:
            mf.addNote(0, 9, KICK, base + b, 0.15, 110 if b == 0 else 98)
        mf.addNote(0, 9, SNARE, base + 2, 0.12, 105)
        mf.addNote(0, 9, CLAP, base + 2.02, 0.1, 92)
        if bar >= 2:
            mf.addNote(0, 9, SNARE, base + 3.5, 0.08, 78)
        if bar in (1, 3):
            mf.addNote(0, 9, RIM, base + 1, 0.06, 82)
            mf.addNote(0, 9, RIM, base + 3, 0.06, 82)
        for i in range(16):
            beat = base + i * 0.25
            if bar == 3 and i >= 13:
                mf.addNote(0, 9, CHH, beat, 0.05, 65 + (i - 13) * 12)
                continue
            vel = 100 if i % 4 == 0 else (78 if i % 2 == 0 else 58)
            note = OHH if i == 14 else CHH
            mf.addNote(0, 9, note, beat, 0.06, vel)
        if bar == 3:
            mf.addNote(0, 9, OHH, base + 3.5, 0.18, 90)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_bass_short(path: Path, bars: int = 4) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "808 short F#")
    roots = [42, 42, 49, 47]
    for bar in range(bars):
        base = bar * 4
        root = roots[bar]
        mf.addNote(0, 0, root, base, 3.5, 105)
        mf.addNote(0, 0, root, base + 2, 0.3, 88)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_drums(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Hyperpop Drums 138")
    for bar in range(BARS):
        base = bar * 4
        for b in (0, 1.5, 2.75):
            mf.addNote(0, 9, KICK, base + b, 0.18, 100)
        mf.addNote(0, 9, SNARE, base + 2, 0.14, 96)
        mf.addNote(0, 9, CLAP, base + 2, 0.11, 88)
        if bar % 2 == 1:
            mf.addNote(0, 9, SNARE, base + 3.5, 0.1, 72)
        for i in range(16):
            beat = base + i * 0.25
            vel = 92 if i % 2 == 0 else 68
            note = OHH if i in (6, 14) else CHH
            mf.addNote(0, 9, note, beat, 0.07, vel)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_bass(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "808 Bass F#maj")
    roots = [42, 49, 51, 47, 42, 44, 49, 47]
    for bar in range(BARS):
        base = bar * 4
        root = roots[bar % len(roots)]
        mf.addNote(0, 0, root, base, 1.85, 100)
        mf.addNote(0, 0, root, base + 2.5, 0.4, 80)
        if bar in (3, 7):
            mf.addNote(0, 0, root + 12, base + 3.25, 0.3, 78)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_chords(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Chords F#maj")
    prog = [Fsh_maj, Csh_maj, Dsh_min, B_maj, Fsh_maj, Gsh_min, Csh_maj, B_maj]
    for bar in range(BARS):
        base = bar * 4
        chord = prog[bar % len(prog)]
        for n in chord:
            mf.addNote(0, 0, n, base, 3.75, 70)
        for n in chord:
            mf.addNote(0, 0, n + 12, base, 3.75, 50)
    with path.open("wb") as f:
        mf.writeFile(f)


def write_stabs(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Stabs F#maj")
    hits = [(0, Fsh_maj), (2, B_maj), (4, Csh_maj), (6, Dsh_min)]
    for bar in range(BARS):
        base = bar * 4
        for beat_off, chord in hits:
            t = base + beat_off
            if t >= total_beats():
                continue
            for n in chord:
                mf.addNote(0, 0, n + 12, t, 0.35, 85)
    with path.open("wb") as f:
        mf.writeFile(f)


def main() -> None:
    write_beat_ayesha_short(OUT / "00_beat_ayesha_4bars.mid")
    write_bass_short(OUT / "00_bass_ayesha_4bars.mid")
    write_drums(OUT / "01_drums_hyperpop.mid")
    write_bass(OUT / "02_bass_808_F#maj.mid")
    write_chords(OUT / "03_chords_F#maj.mid")
    write_stabs(OUT / "04_stabs_hook.mid")
    print(f"OK @ {BPM} BPM → {OUT}")


if __name__ == "__main__":
    main()
