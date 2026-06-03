# Пакет под луп **PLX_MTP_138_synth_arp — F#maj**

Твой клип уже **арпеджио на 138 BPM** — ближе к hyperpop, чем старый piano-луп 87 BPM.

## Warp для этого сэмпла

1. Двойной клик по клипу → **Warp ON**
2. **Seg. BPM = 138** (как в имени файла)
3. **Темп проекта = 138** (или 145–150, если хочешь ещё агрессивнее — тогда Warp подтянет арп)
4. **Warp Mode:** **Tones** или **Complex** (синт-арп, не Beats)
5. ПКМ на первый удар арпа → **Set 1.1.1 here** / **Warp from here (Straight)**

## MIDI-файлы

| Файл | Назначение |
|------|------------|
| `01_drums_hyperpop.mid` | Барабаны |
| `02_bass_808_F#maj.mid` | 808 в F# major |
| `03_chords_F#maj.mid` | Пэды/аккорды (тихо под арп) |
| `04_stabs_hook.mid` | Короткие удары в припев — **можно выключить**, если луп уже перегружает |

## Сборка в Ableton

1. **Трек 1 (Audio):** твой луп → EQ → **Saturator** → **OTT** → sidechain с kick
2. **Трек 2:** `01_drums` → Drum Rack (808 kit)
3. **Трек 3:** `02_bass` → Operator / 808, **моно**
4. **Трек 4:** `03_chords` → Wavetable pad, **−6…−10 dB** (не спорить с арп)
5. **Трек 5:** `04_stabs` — только в припеве или mute

## Стиль Ayesha — что добавить руками

- **Auto Filter** на луп (LFO 1/4)
- **Redux** или **Erosion** на дробных тактах
- **Slice** лупа → 2–3 глитч-куска в дропе
- Вокал: pitch up + OTT + короткий delay

## Перегенерировать

```bash
python3 generate.py
```

## Короткий бит Ayesha (4 такта)

- **`00_beat_ayesha_4bars.mid`** — только ударные (loop 4 bars)
- **`00_bass_ayesha_4bars.mid`** — 808 F# под бит

**Импорт:** MIDI-трек → **Drum Rack** (808) → перетащи beat. Второй трек → Operator → bass MIDI.

**Loop:** включи Loop на 4 такта, темп **138**.

### Схема бита (один такт = 4 доли)

```
Kick:  x . x . | x . . x |  (синкопа, не диско)
Snare: . . x . |  (на 3-й доле)
Clap:  вместе со snare
Hats:  x x x x | x x x x |  (шестнадцатые)
Rim:   . x . x |  (такты 2 и 4)
Такт 4: хэт-ролл в конце + open hat
```

### Обработка (стиль Ayesha)

Drum bus: **OTT** → **Saturator** → **Glue** → sidechain на луп.
