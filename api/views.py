from api import app


@app.route('/',methods=['GET'])
def index():
    return "Hello world"