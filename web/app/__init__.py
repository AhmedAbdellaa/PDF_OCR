from flask import Flask
# from app import tasks,views,config
print("********************************************************before init********************************************************")

app = Flask(__name__)
app.config["ENV"] =="production"
print("********************************************************init********************************************************")
if app.config["ENV"] == "production"  :
    app.config.from_object("config.ProductionConfig")

elif app.config["ENV"] == "testin"  :
    app.config.from_object("config.TestingConfig")
else  :
    app.config.from_object("config.DeveolpmentConfig")


from app import tasks,views
