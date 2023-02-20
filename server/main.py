from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './miami'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# checks to make sure that the file  uploaded has the correct extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/img', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
        if 'file' not in request.files:
            flash('No file part')
   # temporary get call if there is no post on the /img endpoint
    return render_template('index.html')

@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()


# @app.route('/postimage',methods = ['POST'])
# def login():
#    if request.method == 'POST':
#       user = request.form['']
#       return redirect(url_for('success',name = user))
   
app.run('0.0.0.0', port=8080)