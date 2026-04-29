from flask import Flask, request, render_template
import boto3, os

app = Flask(__name__)
polly = boto3.client('polly', region_name='us-west-2')

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form['text']
        if text.strip():
            try:
                response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
                os.makedirs("static", exist_ok=True)
                audio_file = 'static/output.mp3'
                with open(audio_file, 'wb') as f:
                    f.write(response['AudioStream'].read())
            except Exception as e:
                return f"<p>Error: {e}</p>"
    return render_template('index.html', audio=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
