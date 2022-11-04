#------------------importing library---------------------------
from app import app 
from flask import render_template, request,redirect,jsonify,make_response,after_this_request,abort,send_file
from app.tasks import join_read
from werkzeug.utils import secure_filename
import secrets 

#---------------------------------------------------------------------------
#-------------------------------------------------------------------------
#upload file 
import os
import logging
# from pydrop.config import config

print("********************************************************views********************************************************")


@app.route("/",methods=["POST","GET"])
def upload_pdf():
    if request.method == "POST" :
        # print("****************************post***************") 
        if request.files and request.form["dir_name"]:

            group_directory = request.form["dir_name"]

            if not os.path.isdir(os.path.join(app.config["PDF_UPLOADS"],group_directory)):
                os.mkdir(os.path.join(app.config["PDF_UPLOADS"],group_directory))

            file = request.files["file"]
            if os.path.splitext(file.filename)[1] != '.pdf' :
                print( os.path.splitext(file.filename)[1])
                print("only pdf allowed")
                return redirect(request.url)
            else :
                filename = f"{secure_filename(file.filename)}"
                save_path =os.path.join(app.config["PDF_UPLOADS"],group_directory,filename)
                try:
                    with open(save_path, "ab") as f:
                        f.seek(int(request.form["dzchunkbyteoffset"]))
                        f.write(file.stream.read())

                    return redirect(request.url,200)
                except OSError:
                    return "error uploading file try again later",500

    elif request.method=="GET":
        generated_key = secrets.token_urlsafe(6)
        return render_template("public/upload_pdf.html",dir_name=generated_key)

@app.route("/delete",methods=["POST"])
def delete_file():
    if request.method == "POST" :
        if request.form :
            req = request.form
            dir_path =os.path.join(app.config["PDF_UPLOADS"],req["dir_name"])
            file_path = os.path.join(dir_path,secure_filename(req["file_name"] ))
            if os.path.isdir(dir_path):
                print("**********************************dir*******************************")
                try:
                    os.remove(file_path)

                except :
                    print("file not exist")
                finally:
                    if len(os.listdir(dir_path)) == 0:
                        os.rmdir(dir_path)
                        return redirect(request.url,200)     
    return make_response(jsonify({"output_path": "asdf"}), 200)     

#---------------------------------------------------------------
#sending file
@app.route("/send",methods=["GET","POST"])
def send():
    req = request.form
    dir_path =os.path.join(app.config["PDF_UPLOADS"],req["dir_name"])
    output_path = os.path.join(app.config["CLIENT_FOLDER"],f'{secrets.token_urlsafe(6)}_ocr.pdf',)
    
    if join_read(dir_path,output_path):
        try:
            
            return make_response(jsonify({"output_path": output_path}), 200) 

        except FileNotFoundError:
            abort(404)
    else :
        return make_response(jsonify({"message": "succsseed"}), 500) #internel server error
  
#---------------------------------------------------------------

@app.route("/pdfViewer",methods=["GET","POST"])
def view_pdf():
    output_path= os.path.join(request.form["output_path"])
    return send_file(output_path,as_attachment=False)

