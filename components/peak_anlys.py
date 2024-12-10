import numpy as np
import matplotlib.pyplot as plt
import peakutils
import librosa
from scipy.signal import hilbert

def display_adjusted_wave(audio_path, output_path):

    y, sample_rate = librosa.load(audio_path, sr=None)

    times = np.linspace(0, len(y) / sample_rate, len(y))

    # skip the first 0.5 seconds of the audio to avoid noise
    start_sample = int(0.5 * sample_rate)
    y = y[start_sample:]
    times = times[start_sample:]

    # calculate the envelope of the audio using the hilberts
    analytic_signal = hilbert(y)
    amplitude_envelope = np.abs(analytic_signal)

    # smoothen the wave(simple moving average)
    window_size = int(sample_rate * 0.05)
    smoothed_envelope = np.convolve(amplitude_envelope, np.ones(window_size) / window_size, mode='same')

    # normalize the graph
    smoothed_envelope_normalized = smoothed_envelope / np.max(smoothed_envelope)

    # Set minimum distance between peaks (0.5 seconds)
    min_dist = sample_rate * 0.5

    # detect peaks using peakutils
    initial_peaks = peakutils.indexes(smoothed_envelope_normalized, thres=0.1, min_dist=int(min_dist))

    # calculate the average amplitude of the smoothed envelope
    average_amplitude = np.mean(smoothed_envelope_normalized)

    # filter peaks above average amplitude
    def filter_above_average(peaks, envelope, avg_amp):
        return np.array([peak for peak in peaks if envelope[peak] > avg_amp])

    above_average_peaks = filter_above_average(initial_peaks, smoothed_envelope_normalized, average_amplitude)

    # filter peaks to ensure they are almost equally spaced
    def filter_equally_spaced_peaks(peaks, min_spacing):
        filtered_peaks = [peaks[0]]
        for i in range(1, len(peaks)):
            if peaks[i] - filtered_peaks[-1] >= min_spacing:
                filtered_peaks.append(peaks[i])
        return np.array(filtered_peaks)
    
    target_spacing = sample_rate * 2 
    peaks = filter_equally_spaced_peaks(above_average_peaks, target_spacing * 0.7)


    plt.style.use('dark_background')
    plt.figure(figsize=(10, 4))
    plt.plot(times, smoothed_envelope, label='Smoothed Envelope', linewidth=2)
    plt.plot(times[peaks], smoothed_envelope[peaks], 'go', label='Filtered Peaks (Evenly Spaced, Above Average)')
    plt.axhline(y=average_amplitude, color='r', linestyle='--', label='Average Amplitude')
    plt.title('Smoothed Envelope with Filtered Peaks')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(output_path)
    plt.close()

    num_peaks = len(peaks)
    duration_in_seconds = len(y) / sample_rate
    peaks_per_minute = (num_peaks / duration_in_seconds) * 60
    return peaks_per_minute
