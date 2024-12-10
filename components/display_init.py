# display_init.py
import numpy as np
import matplotlib.pyplot as plt
import librosa

def display_initial_wave(audio_path, output_path):

    y, sample_rate = librosa.load(audio_path, sr=None)
    

    times = np.linspace(0, len(y) / sample_rate, len(y))

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 4))
    plt.plot(times, y, label='Original Sound Wave')
    plt.title('Original Sound Wave')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    
    # save the plot as an image
    plt.savefig(output_path)
    plt.close()
