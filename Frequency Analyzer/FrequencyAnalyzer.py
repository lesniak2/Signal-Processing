import pylab, scipy
import numpy as np
from scipy.io import wavfile
import Image
import json


def stft(x, fs, framesz, hop):
    """
    Short-time fourier transform an input
    """
    framesamp = int(framesz*fs)
    hopsamp = int(hop*fs)
    w = scipy.hamming(framesamp)
    X = scipy.array([scipy.fft(w*x[i:i+framesamp]) for i in range(0, len(x)-framesamp, hopsamp)])
    return X


def calculate_weights(data):
    weights = []
    low_count = mid_count = high_count = 0
    # Use piano octaves to determine low-high frequencies
    for x in data:
        if x < 200:
            low_count += 1
        elif 200 <= x < 400:  # the octave around the piano's middle-C
            mid_count += 1
        else:
            high_count += 1

    total = float(len(data))
    for x in data:
        if x < 200:
            weights.append(low_count/total)
        elif 200 <= x < 400:
            weights.append(mid_count/total)
        else:
            weights.append(high_count/total)
    return weights


# Plot the magnitude spectrogram.
def show_spec(data):
    pylab.figure()
    pylab.imshow(scipy.absolute(data.T), origin='lower', aspect='auto',
                 interpolation='nearest')
    pylab.xlabel('Time')
    pylab.ylabel('Frequency')
    pylab.show()


# take the absolute frequencies and only include
# frequencies in the melodic range (40-4000Hz)
# Replace rest with -1
def cleanse(data):
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            abs = scipy.absolute(data[i][j])
            if not (40 <= abs <= 4000):
                data[i][j] = -1.0
            else:
                data[i][j] = abs
    return np.real(data)


def freq_to_rgb(freq):
    #todo: set a a base color then adjust brightness to produce
    brightness = freq/4000.0
    r = g = b = int((brightness * 255))
    return r, g, b


if __name__ == '__main__':

    sample_rate, raw_data = wavfile.read('Adele-Turning Tables.wav')
    frame_size = 0.050
    hop = 0.150

    freq_data = stft(raw_data, sample_rate, frame_size, hop)
    cleansed_data = cleanse(freq_data)

    d = {}
    time = 0.0
    for time_slot in cleansed_data:
        filtered_data = [freq for freq in time_slot if freq != -1.0]
        if len(filtered_data) > 0:
            weights = calculate_weights(filtered_data)
            d[round(time, 2)] = freq_to_rgb(int(np.average(filtered_data, weights=weights)))
        time += hop

    with open('Adele-Turning Tables.json', 'w') as outfile:
        json.dump(d, outfile, sort_keys=True, indent=4)

 #code to generate an image
    width = len(d.keys())
    height = 600

    img = Image.new("RGB", (width, height))
    col = 0
    time = min(d)
    while col < width:
        r, g, b = d[round(time, 2)]
        row = 0
        while row < height:
            img.putpixel((col, row), (r, g, b))
            row += 1
        col += 1
        time += hop
    img.save("with weights.png", "PNG")
