# Стартовый пакет под стиль Ayesha Erotica (Ableton)

Готовый **трек целиком** из облака сделать нельзя — нет доступа к твоему Ableton и к файлу лупа Birocratic.  
Здесь — **4 MIDI-файла** (150 BPM, C minor), которые ты подкладываешь **под свой warped-луп**.

## Файлы

| Файл | Назначение |
|------|------------|
| `01_drums_hyperpop.mid` | Kick, snare, clap, hi-hats |
| `02_bass_808_Cm.mid` | Бас-линия (назначь Operator / 808) |
| `03_chords_Cm.mid` | Аккорды Cm–Ab–Eb–Bb (Wavetable pluck/pad) |
| `04_arp_lead.mid` | Арпеджио для припева |

## Быстрый импорт в Ableton

1. **Темп проекта:** 150 BPM.
2. Твой луп: **Warp ON**, **Seg. BPM 87**, режим **Complex** или **Tones**.
3. Перетащи все `.mid` из этой папки на отдельные MIDI-треки.
4. **Drums:** Drum Rack (808 Core или свой kit). MIDI channel 10 подхватится сам.
5. **Bass:** Operator → Bass / 808 preset, моно, sidechain с kick.
6. **Chords:** Wavetable → Pluck, короткий decay, OTT + Saturator.
7. **Arp:** яркий lead, только в припеве (mute в куплете).

## Обработка лупа (напоминание)

EQ → Saturator → OTT → Glue → sidechain с kick.

## Структура (8 тактов = 1 цикл MIDI)

- Такты 1–4: куплет — drums тихо, без arp.
- Такты 5–8: припев — всё + arp, OTT громче.

Склей 4–8 циклов в Arrangement → intro / break / drop по вкусу.

## Перегенерировать

```bash
python3 generate.py
```
