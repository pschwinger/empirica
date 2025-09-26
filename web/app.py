from flask import Flask, render_template, abort
import os

app = Flask(__name__, static_folder='dist', static_url_path='')

@app.route('/')
@app.route('/<path:path>')
def serve(path='index.html'):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
