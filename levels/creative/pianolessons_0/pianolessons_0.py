from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

p = Piano.first()
e = DataExchange.first()
notes = e.get_data("MidiNotes")

def midi_to_note(midi_note):
    note_names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    octave = (midi_note // 12) - 1
    note_name = note_names[midi_note % 12]
    return f"{note_name}{octave}"

for midi_note in notes:
    key_octave = midi_to_note(midi_note)
    p.play_note(key_octave)
    sleep(0.1)
