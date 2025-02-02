from pydub import AudioSegment

# Load audio file
audio = AudioSegment.from_file("ALGIDO.WAV")

def pitch_shift(audio, semitones):
    # Adjust sample rate to shift pitch
    new_sample_rate = int(audio.frame_rate * (2.0 ** (semitones / 12.0)))
    return audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio.frame_rate)


# Speed up (by a factor of 1.5)
speed_up_audio = audio.speedup(playback_speed=1.1)
slowed_down_audio = pitch_shift(audio, -1)

# Slow down (by a factor of 0.7)

# Export the modified audio to a new file
speed_up_audio.export("speed_up_output_ALGIDO.mp3", format="mp3")
slowed_down_audio.export("algidoSlow.mp3", format="mp3")