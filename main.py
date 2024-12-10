import os
from flask import Flask, render_template, request
from components.display_init import display_initial_wave
from components.peak_anlys import display_adjusted_wave

UPLOAD_FOLDER = 'audio/'
OUTPUT_FOLDER = 'static/outputs/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # for saving audio file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # for generate initial and adjusted wave figs
            initial_output_path = os.path.join(OUTPUT_FOLDER, 'initial_wave.png')
            adjusted_output_path = os.path.join(OUTPUT_FOLDER, 'adjusted_wave.png')

            display_initial_wave(file_path, initial_output_path)
            peaks_per_minute = display_adjusted_wave(file_path, adjusted_output_path)

            # analyse breath rate based on intervals of 4
            standard_breath_rate = 14
            rate_difference = peaks_per_minute - standard_breath_rate

            if rate_difference <= -8:
                breath_status = "Very slow"
            elif rate_difference <= -4:
                breath_status = "Slow"
            elif rate_difference <= 4:
                breath_status = "Perfect"
            elif rate_difference <= 8:
                breath_status = "Fast"
            else:
                breath_status = "Very fast"

            # render the output template with images and analysis
            return render_template('display.html', 
                                   initial_image='outputs/initial_wave.png', 
                                   adjusted_image='outputs/adjusted_wave.png', 
                                   peaks_per_minute=peaks_per_minute, 
                                   breath_status=breath_status)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
