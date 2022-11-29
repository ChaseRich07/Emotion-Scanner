from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
from os.path import dirname, exists
from werkzeug.utils import secure_filename
from deepface import DeepFace
from pathlib import Path
import cv2

UPLOAD_FOLDER = (dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    path = (os.path.abspath(filename))
    path = os.path.dirname(path)
    path = (repr(path))
    imgpath = ((dirname(__file__)) + "\\" + filename)
    image = cv2.imread(imgpath)
    analyze = DeepFace.analyze(image)
    analyze = (analyze['dominant_emotion'])

    return render_template('index.html', variable = analyze)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global file
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = (os.path.abspath(filename))
            path = os.path.dirname(path)
            path = (repr(path))
            path = path.replace(" ","_")


            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload an image of a human face to scan</h1>
    <b>This test will display the most dominant emotion in the uploaded image</b>
    <p>Upon uploading, you will be redirected and the results will be displayed.</p>
    <p>If more than one face is in the image, the program will display the most dominant emotion amongst all faces</p>
    <p>Please ensure that the image is either .jpg, .jpeg, or .png</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
