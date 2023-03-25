from flask import Flask
from flask import render_template, send_file
from flask import request
from flask import redirect
import boto3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './files'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'jpeg'

def securefilename(filename):
    return filename.replace(" ", "")


@app.route('/')
def index():
    index_html = """
    <form method="post" enctype="multipart/form-data" action="/upload" method="post">
<div>
<label for="file">Choose file to upload</label>
<input type="file" id="file" name="form_file" accept="image/jpeg"/>
</div>
<div>
<button>Submit</button>
</div>
</form>
<style>
body{
background-color:#ADD8E6;
}
</style>
    """
    s3_client = boto3.client('s3', aws_access_key_id='AKIAWZATVY7MB4BXAOIG', aws_secret_access_key= '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')
    file_names = []
    response = s3_client.list_objects_v2(Bucket="chefomardee-testing")
    try:
        for obj in response['Contents']:
            file_names.append(obj['Key'])
        print(file_names)
        for i in (file_names):
            s3_client.download_file("chefomardee-testing", i, './files2/'+i)  
        
        for file in list_files():
            index_html += "<li><a href=\"/files2/" + file + "\">" + file + "</a></li>"

        return index_html
    except:
        return index_html


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # print('upload')
    file = request.files['form_file'] 
    file.save(os.path.join("./files", file.filename))
    
    s3_client = boto3.client('s3', aws_access_key_id='AKIAWZATVY7MB4BXAOIG', aws_secret_access_key= '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')
    s3_client.upload_file(os.path.join("./files", file.filename), "chefomardee-testing", file.filename)

    return redirect("/")


@app.route('/files2')
def list_files():
    # print("GET /files")
    files = os.listdir("./files2")
    jpegs = []
    # print(files)
    for file in files:
        # print(file)
        # print(file.endswith(".jpeg"))
        if not file.endswith(".jpeg"):
            jpegs.append(file)
    # print(jpegs)
    return files


@app.route('/files2/<filename>')
def get_file(filename):

    return send_file(os.path.join("./files2/", filename))



app.run(host="0.0.0.0", port=3000)


