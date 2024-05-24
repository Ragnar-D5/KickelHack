## Benzaiten ##

(temporary App-name)

save all requirements:

`pip freeze > requirements.txt`

install all requirements:

`pip install -r /path/to/requirements.txt`

**GUI**

- [ ] Tabsystem
  - [ ] Tabs work
  - [ ] dropdown menus (save,open,import,export file / choose intrument)
- [ ] Arrangment:
  - [ ] drag/drop blocks on multiple Timelines (like FL Studio)
  - [ ] optional: visualize MIDI/WAV-Data (like FL Studio)
- [ ] Compose:
  - [ ] place notes to create blocks
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
  - [ ] Realtime playing
  - [ ] optional: save/open/etc.
  - [ ] optional: record play with keys link piano
- [ ] Instrument:
  - [ ] optional: save instrument-setting (json idk)
- [ ] optional: Setting
- [ ] only if necessary: complete GUI

(not necessesarily in Order; no need for polish)


**BACKEND-Math**

- [ ] Base-Synthesis
  - [ ] Generate frequency modulated waves (sine,square,sawtooth,harmonic) + files as np.arrays
  - [ ] adding Sounds together/global np.array
  - [ ] louder/quieter/fade in/out/splice/echo/delay/speed change/pitch shift (important for other stuff)
  - [ ] optional: fluid pitch shift
  - [ ] noise gen
  - [ ] downsampling
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
