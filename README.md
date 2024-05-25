## Benzaiten (preliminary App-name) ##

save all requirements:

`pip freeze > requirements.txt`

install all requirements:

`pip install -r /path/to/requirements.txt`

**GUI**

- [ ] Tabsystem
  - [ ] Tabs work (like Bosca Ceoil)
  - [ ] dropdown menus (save,open,import,export file / choose intrument)
- [ ] Arrangment:
  - [ ] drag/drop blocks on multiple Timelines (like FL Studio)
  - [ ] optional: visualize MIDI/WAV-Data (like FL Studio)
- [ ] Compose:
  - [ ] place notes to create blocks (like Bosca Ceoil)
  - [ ] scrollable Notelines (like Bosca Ceoil)
  - [ ] optional: play with keys link piano
- [ ] Instrument:
  - [ ] button or similar new fequency + slider for frequency amplitude
  - [ ] optional: visualize Wave
- [ ] optional: Setting

(not necessesarily in Order; no need for polish)


**BACKEND-Bridge**

- [ ] Import/Export/etc.
  - [x] Import MIDI/WAV
  - [ ] Export WAV
  - [ ] optional: Export note-Blocks as MIDI
  - [ ] optional: save/open/etc.
  - [ ] optional: record play with keys link piano
- [ ] Instrument:
  - [ ] save/open instrument-setting (json idk, or do similar with hardcoding ig)
- [ ] optional: Setting
- [ ] nvm mainly your task now: complete GUI

(not necessesarily in Order; no need for polish)


**BACKEND-Math**

- [ ] Base-Synthesis
  - [ ] Generate frequency modulated waves (sine,square,sawtooth,harmonic) + files as np.arrays
  - [ ] adding Sounds together/global np.array
  - [ ] my task now: Realtime playing
  - [ ] louder/quieter/fade in/out/splice/echo/delay/speed change/pitch shift (important for other stuff)
  - [ ] optional: fluid pitch shift
  - [ ] arpeggio/noise gen
  - [ ] downsampling/vocoder
  - [ ] optional: extra special effects
  - [ ] bandwidth reduction/modulation (maybe by code, cause dragging bezier is a pain and cringe)
  - [ ] optional: custom fades (maybe by code, cause dragging bezier is a pain and cringe)
- [ ] Instrument-Synthesis
  - [ ] smol custom sound palette (like 4 or 5) with frequency vectors
  - [ ] play midi with custom sounds
  - [ ] handle percussion seperatly (its easier i hope)

(not necessesarily in Order; no need for polish)

**Culmination**

- [ ] short musicdemo
