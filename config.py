import os

class Config:

    QUOTES_API = 'http://quotes.stormconsultancy.co.uk/random.json'
    SECRET_KEY = os.environ.get('wefrwefdsc34343')
    SQLALCHEMY_DATABASE_URI = 'postgres://vyvqzszajrmrui:b082c9f3c61b7ac2836067a8ea395c8a20c8723e96b91b79c812257d3b000c5b@ec2-54-221-214-183.compute-1.amazonaws.com:5432/d2hgsc2qvoielo'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
class ProdConfig(Config):
     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") 


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://vyvqzszajrmrui:b082c9f3c61b7ac2836067a8ea395c8a20c8723e96b91b79c812257d3b000c5b@ec2-54-221-214-183.compute-1.amazonaws.com:5432/d2hgsc2qvoielo'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://vyvqzszajrmrui:b082c9f3c61b7ac2836067a8ea395c8a20c8723e96b91b79c812257d3b000c5b@ec2-54-221-214-183.compute-1.amazonaws.com:5432/d2hgsc2qvoielo'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}
