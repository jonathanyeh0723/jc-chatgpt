from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    videos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'video' not in request.files:
            return redirect(request.url)
        
        video = request.files['video']
        
        if video.filename == '':
            return redirect(request.url)
        
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))
        
        return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)

