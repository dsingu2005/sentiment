from flask import Flask, request, render_template, send_from_directory
from google.cloud import storage
import os
import main

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\haris\OneDrive\Desktop\sem2\sentiment\12_20\sentiment-analysis-379200-85d47d170d69.json'

storage_client = storage.Client()
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        folder = request.form.get('dropdown')
        urls = main.process_folder(folder)
        return render_template('display.html', urls=urls)  # Pass the URLs to the template
    else:
        bucket_name = 'sentiment-files'
        blobs = storage_client.list_blobs(bucket_name, prefix='scores_magnitude/')
        files = set(blob.name.split('/')[1] for blob in blobs if '/' in blob.name)
        return render_template('upload.html', folders=files)  # Render the upload.html template

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/display_results/<path:folder_name>')
def display_results(folder_name):
    # Add logic to compile and display results
    main.compile_results(folder_name)
    urls = main.process_folder(folder_name)
    return render_template('display.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
