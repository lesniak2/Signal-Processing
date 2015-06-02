#Frequency Analyzer
Given a .wav input (in this case Adele - Turning Tables was used), creates a JSON with grayscale values
based on the frequencies at a specific time. The analysis is done with a Short-time Fourier Transform
and percieved high and low pitches are based on piano octaves. Higher pitches are more white, lower more black.
The resulting JSON is the RGB specification that resulted from the analyzed time window.