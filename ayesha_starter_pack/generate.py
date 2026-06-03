#!/usr/bin/env python3
"""Hyperpop starter MIDI pack — C minor, 150 BPM (import into Ableton with your loop)."""

from pathlib import Path

from midiutil import MIDIFile

BPM = 150
BARS = 8
OUT = Path(__file__).resolve().parent

# General MIDI drums (channel 10)
KICK, SNARE, CHH, OHH, CLAP = 36, 38, 42, 46, 39

# C minor
Cm, Eb, Gm, Ab, Bb = [60, 63, 67], [63, 67, 70], [67, 70, 74], [68, 72, 75], [70, 74, 77]


def beats_per_bar():
    return 4


def total_beats():
    return BARS * beats_per_bar()


def write_drums(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Hyperpop Drums")
    t = 0

    for bar in range(BARS):
        base = bar * 4
        # Kick — trap/hyperpop pocket
        for b in (0, 1.75, 2.5):
            mf.addNote(0, 9, KICK, base + b, 0.2, 100)
        # Snare / clap
        mf.addNote(0, 9, SNARE, base + 2, 0.15, 95)
        mf.addNote(0, 9, CLAP, base + 2, 0.12, 85)
        mf.addNote(0, 9, SNARE, base + 3.5, 0.1, 70)
        # 16th hats
        for i in range(16):
            beat = base + i * 0.25
            vel = 95 if i % 2 == 0 else 72
            note = OHH if i == 14 else CHH
            mf.addNote(0, 9, note, beat, 0.08, vel)

    with path.open("wb") as f:
        mf.writeFile(f)


def write_bass(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "808 Bass Cm")
    # C2 roots with simple pattern
    roots = [36, 36, 39, 36, 41, 39, 36, 34]  # C Eb G ... Bb Ab F C
    for bar in range(BARS):
        base = bar * 4
        root = roots[bar % len(roots)]
        mf.addNote(0, 0, root, base, 1.9, 100)
        mf.addNote(0, 0, root, base + 2, 0.45, 85)
        if bar % 2 == 1:
            mf.addNote(0, 0, root + 12, base + 3, 0.35, 75)

    with path.open("wb") as f:
        mf.writeFile(f)


def write_chords(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Chords Cm hyperpop")
    prog = [Cm, Ab, Eb, Bb, Cm, Gm, Ab, Eb]
    for bar in range(BARS):
        base = bar * 4
        chord = prog[bar % len(prog)]
        for n in chord:
            mf.addNote(0, 0, n + 12, base, 3.8, 78)
        for n in chord:
            mf.addNote(0, 0, n + 24, base, 3.8, 55)

    with path.open("wb") as f:
        mf.writeFile(f)


def write_arp(path: Path) -> None:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, BPM)
    mf.addTrackName(0, 0, "Arp lead")
    notes = [60, 63, 67, 72, 67, 63, 68, 75, 70, 74, 77, 74]
    step = 0.25
    idx = 0
    t = 0
    while t < total_beats() - step:
        mf.addNote(0, 0, notes[idx % len(notes)], t, step * 0.9, 82)
        t += step
        idx += 1

    with path.open("wb") as f:
        mf.writeFile(f)


def main() -> None:
    write_drums(OUT / "01_drums_hyperpop.mid")
    write_bass(OUT / "02_bass_808_Cm.mid")
    write_chords(OUT / "03_chords_Cm.mid")
    write_arp(OUT / "04_arp_lead.mid")
    print(f"Wrote 4 MIDI files to {OUT} @ {BPM} BPM")


if __name__ == "__main__":
    main()
