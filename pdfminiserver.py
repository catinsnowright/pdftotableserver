import os
import logging
import threading
import pandas as pd
import tabula
from flask import Flask, jsonify, request, send_file
from PyPDF2 import PdfFileReader

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/output'
app.config['PDF_SERVER_IP'] = '192.168.0.1'
app.config['PDF_SERVER_PORT'] = 5000
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

logging.basicConfig(filename='/var/log/pdfminiserver.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def pdf_to_csv_json(filepath, output_format):
    with open(filepath, 'rb') as f:
        if output_format == 'csv':
            return tabula.convert_into(f, "output.csv", output_format="csv", pages='all')
        elif output_format == 'json':
            return tabula.convert_into(f, "output.json", output_format="json")
        else:
            return None

class ConvertThread(threading.Thread):
    def __init__(self, filepath, output_format):
        threading.Thread.__init__(self)
        self.filepath = filepath
        self.output_format = output_format

    def run(self):
        try:
            output = pdf_to_csv_json(self.filepath, self.output_format)
            os.remove(self.filepath)
            return output
        except Exception as e:
            logging.error('Error converting PDF file: ' + str(e))

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        output_format = request.form.get('output_format', 'csv')
        thread = ConvertThread(filepath, output_format)
        thread.start()
        return jsonify({'message': 'File uploaded successfully and conversion started.'}), 200
    else:
        return jsonify({'error': 'File type not allowed.'}), 400

if __name__ == '__main__':
    app.run(debug=False, host=app.config['PDF_SERVER_IP'], port=app.config['PDF_SERVER_PORT'], threaded=True)
