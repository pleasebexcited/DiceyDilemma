import wave
import struct
import math
import random

def create_attack_sound():
    """Create a glitchy 16-bit sword hit sound effect"""
    # Audio parameters
    sample_rate = 44100
    duration = 0.15  # 150ms - short and punchy
    frequency = 200  # Lower base frequency
    amplitude = 0.7  # Louder
    
    # Generate audio data
    num_samples = int(sample_rate * duration)
    audio_data = []
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Create a harsh square wave
        square_wave = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
        
        # Add noise for glitch effect
        noise = (random.random() - 0.5) * 0.3
        
        # Add harsh harmonics
        harmonic1 = 0.5 * (1.0 if math.sin(2 * math.pi * frequency * 3 * t) > 0 else -1.0)
        harmonic2 = 0.3 * (1.0 if math.sin(2 * math.pi * frequency * 5 * t) > 0 else -1.0)
        harmonic3 = 0.2 * (1.0 if math.sin(2 * math.pi * frequency * 7 * t) > 0 else -1.0)
        
        # Add some frequency modulation for glitch
        fm_offset = 50 * math.sin(2 * math.pi * 20 * t)  # 20Hz modulation
        fm_wave = 1.0 if math.sin(2 * math.pi * (frequency + fm_offset) * t) > 0 else -1.0
        
        # Combine all elements
        combined_wave = square_wave + harmonic1 + harmonic2 + harmonic3 + fm_wave + noise
        
        # Apply harsh envelope - very sharp attack, quick decay
        envelope = 1.0
        if t < 0.02:  # Very sharp attack
            envelope = t / 0.02
        else:  # Very quick decay
            envelope = 1.0 - ((t - 0.02) / (duration - 0.02)) * 0.9
        
        # Add some distortion/clipping
        sample = amplitude * envelope * combined_wave
        sample = max(-1.0, min(1.0, sample))  # Clip to prevent overflow
        
        audio_data.append(int(sample * 32767))
    
    # Write WAV file
    with wave.open("sounds/attack.wav", "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(struct.pack(f"<{len(audio_data)}h", *audio_data))

def create_power_up_sound():
    """Create a glitchy 16-bit power-up sound effect"""
    # Audio parameters
    sample_rate = 44100
    duration = 0.4  # 400ms
    amplitude = 0.8  # Louder
    
    # Generate audio data
    num_samples = int(sample_rate * duration)
    audio_data = []
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Create a glitchy arpeggio
        progress = t / duration
        
        # Four harsh notes in sequence
        if progress < 0.25:
            # First note - harsh
            note_progress = progress / 0.25
            frequency = 300 + (500 - 300) * note_progress
        elif progress < 0.5:
            # Second note - glitchy
            note_progress = (progress - 0.25) / 0.25
            frequency = 500 + (700 - 500) * note_progress
        elif progress < 0.75:
            # Third note - crunchy
            note_progress = (progress - 0.5) / 0.25
            frequency = 700 + (900 - 700) * note_progress
        else:
            # Fourth note - harsh finale
            note_progress = (progress - 0.75) / 0.25
            frequency = 900 + (1200 - 900) * note_progress
        
        # Create harsh square wave
        square_wave = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
        
        # Add noise for glitch effect
        noise = (random.random() - 0.5) * 0.2
        
        # Add harsh harmonics
        harmonic1 = 0.4 * (1.0 if math.sin(2 * math.pi * frequency * 3 * t) > 0 else -1.0)
        harmonic2 = 0.3 * (1.0 if math.sin(2 * math.pi * frequency * 5 * t) > 0 else -1.0)
        
        # Add frequency modulation for glitch
        fm_offset = 30 * math.sin(2 * math.pi * 15 * t)
        fm_wave = 1.0 if math.sin(2 * math.pi * (frequency + fm_offset) * t) > 0 else -1.0
        
        # Combine waves
        combined_wave = square_wave + harmonic1 + harmonic2 + fm_wave + noise
        
        # Apply envelope
        envelope = 1.0
        if t < 0.02:  # Sharp attack
            envelope = t / 0.02
        else:  # Quick decay
            envelope = 1.0 - ((t - 0.02) / (duration - 0.02)) * 0.7
        
        # Add distortion
        sample = amplitude * envelope * combined_wave
        sample = max(-1.0, min(1.0, sample))  # Clip
        
        audio_data.append(int(sample * 32767))
    
    # Write WAV file
    with wave.open("sounds/power_up.wav", "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(struct.pack(f"<{len(audio_data)}h", *audio_data))

def create_death_sound():
    """Create a satisfying enemy death sound effect"""
    # Audio parameters
    sample_rate = 44100
    duration = 0.6  # 600ms
    amplitude = 0.8
    
    # Generate audio data
    num_samples = int(sample_rate * duration)
    audio_data = []
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Create a descending tone (death sound)
        progress = t / duration
        frequency = 800 - (progress * 600)  # Descend from 800Hz to 200Hz
        
        # Create harsh square wave
        square_wave = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
        
        # Add noise for glitch effect
        noise = (random.random() - 0.5) * 0.4
        
        # Add harmonics
        harmonic1 = 0.3 * (1.0 if math.sin(2 * math.pi * frequency * 2 * t) > 0 else -1.0)
        harmonic2 = 0.2 * (1.0 if math.sin(2 * math.pi * frequency * 3 * t) > 0 else -1.0)
        
        # Combine waves
        combined_wave = square_wave + harmonic1 + harmonic2 + noise
        
        # Apply envelope - slow decay
        envelope = 1.0
        if t < 0.05:  # Sharp attack
            envelope = t / 0.05
        else:  # Slow decay
            envelope = 1.0 - ((t - 0.05) / (duration - 0.05)) * 0.5
        
        # Add distortion
        sample = amplitude * envelope * combined_wave
        sample = max(-1.0, min(1.0, sample))  # Clip
        
        audio_data.append(int(sample * 32767))
    
    # Write WAV file
    with wave.open("sounds/death.wav", "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(struct.pack(f"<{len(audio_data)}h", *audio_data))

if __name__ == "__main__":
    import os
    
    # Create sounds directory if it doesn't exist
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
    
    # Generate sound effects
    create_attack_sound()
    create_power_up_sound()
    create_death_sound()
    
    print("Sound effects created successfully!")
    print("- sounds/attack.wav (regular attack sound)")
    print("- sounds/power_up.wav (power-up attack sound)")
    print("- sounds/death.wav (enemy death sound)") 