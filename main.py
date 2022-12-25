from flask import Flask, request, Response, render_template, stream_with_context
import uuid
import gdown
import json
import wget
from Printer import Printer
app = Flask(__name__)
with open('config.json') as f:
    config = json.load(f)
    libpath = config['libpath']
    tmppath = config['tmppath']
    tmp_clean_time = config['tmp_clean_time']
    paper_size = config['paper_size']
    host = config['host']
    port = config['port']
    debug = config['debug']

@app.route('/run', methods=['POST'])
def run():
    print(request.form)
    Type = request.form['Type']
    unique_filename = f"{tmppath}/{str(uuid.uuid4())}.pdf"
    def handle_process():
        try:
            yield f'Type: {Type} <br>'
            if Type == 'gdrive':
                file_id = request.form['id']
                yield f'file_id: {file_id}  <br>'
                gdown.download(
                    id=file_id,
                    output=unique_filename,
                    quiet=False,
                    fuzzy=True)
                yield f'gdown download success  <br>'

            elif Type == 'url':
                url = request.form['id']
                yield f'url: {url}  <br>'
                wget.download(url, unique_filename)
                yield f'wget download success  <br>'
        except Exception as e:
            yield f'Error: {str(e)}  <br>'
            return
        printer = Printer(unique_filename)
        printer.run()
        yield f'printer status: {printer.status} <br>'
        yield f'printer error_list: {printer.error_list} <br>'
    return Response(stream_with_context(handle_process()))

@app.route('/')
def hello():
    return render_template('index.html', now_printer=Printer.get_default_printer())

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
