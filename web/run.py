import os 
# print(os.listdir(os.path.join(os.getcwd(),"app")))
from app import app
from gevent.pywsgi import WSGIServer

if __name__ == '__main__' :
    # print(os.listdir(os.path.join(os.getcwd(),"app")))
    

    port = int(os.environ.get('PORT', 5000))
    print("********************************************************before run********************************************************")
    if not os.path.isdir(app.config["PDF_UPLOADS"]):
        os.mkdir(app.config["PDF_UPLOADS"])

    if not os.path.isdir(app.config["CLIENT_FOLDER"]):
        os.mkdir(app.config["CLIENT_FOLDER"])
    app.run(host="0.0.0.0",port=port)
    # http_server = WSGIServer(('', port), app)
    # http_server.serve_forever()

    print("********************************************************run********************************************************")


    
    # print(app.config)
