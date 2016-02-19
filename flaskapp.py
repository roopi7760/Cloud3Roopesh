import boto3
from flask import Flask, request, session, redirect, url_for, make_response, send_file, render_template,send_from_directory
from werkzeug import secure_filename
import os
from boto3.session import Session

session = Session(aws_access_key_id = '',
                  aws_secret_access_key = '',
                  region_name = '')
s3 = session.resource('s3')
bucketname = ''
LoginFile = ''
application = Flask(__name__)
application.config.from_object(__name__)

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#@app.route('/upload', methods = ['POST', 'GET'])
def upload_file(filename):
    s3.Bucket(bucketname).upload_file(UPLOAD_FOLDER + '/' + filename,filename)
    #os.remove(UPLOAD_FOLDER + '/' + filename)
    #return redirect(url_for('insertFileIntoDB',filename = filename))
    return "Image uploaded successfully"

@application.route('/download/<filename>')
def download_photo(filename):
    return redirect('https://s3-us-west-2.amazonaws.com/<bucketname>/'+filename)

#@application.route('/view/<filename>')
#def view_photo(filename):
    #s3.Bucket(bucketname).download_file(filename, UPLOAD_FOLDER + '/' + filename)
    #return redirect('https://s3-us-west-2.amazonaws.com/roopesh1/' + filename) #send_from_directory(UPLOAD_FOLDER, filename)
#    return render_template('viewimage.html',filename = filename)

@application.route('/delete/<filename>')
def delete_photo(filename):
    s3.Object(bucketname, filename).delete()
    #os.remove(UPLOAD_FOLDER + '/' + filename)
    return render_template('view.html', message = "Image was deleted successfully!", s3=s3, bucketname=bucketname)

@application.route('/home', methods = ['POST', 'GET'])
def home():
    res = ""
    if request.method == 'POST' :
        if (request.form['submit'] == "Upload"):
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                file.close()
                res = upload_file(filename)
            else:
                return render_template('home.html', message = "Either file was not selected or selected file is not an image! Please try again.")
        elif(request.form['submit'] == "View"):
            return render_template('view.html',message = "",s3=s3, bucketname=bucketname)
        else :
            render_template('home.html', message = "")
    return render_template('home.html', message = res)
    #return render_template('home.html', message = message)

@application.route('/',methods = ['POST','GET'])
def login():
    message = ""
    if request.method == 'POST' :
        obj = s3.Object(bucket_name = bucketname, key = LoginFile).get()
        dataFromObj = obj['Body'].read()
        dataFromObj = dataFromObj.split()
        username = request.form['username']
        username = username.lower()
        if  username in dataFromObj :
            #message = "success"
            return render_template('home.html',username = "Welcome " + username.upper() + "!")
        else:
            message = "User name does not exist, Please try again"
            return render_template('index.html', message=message)
    return render_template('index.html', message = message)

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=port)
    application.debug=True
    application.run(debug=True)