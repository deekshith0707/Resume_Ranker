from flask import Flask, render_template, request, redirect, url_for
import os
from ranker import rank_resumes

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('resumes')
    job_desc = request.files['job_desc']

    if job_desc:
        job_desc.save('job_description.txt')

    for file in files:
        if file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

    return redirect(url_for('rank'))

@app.route('/rank')
def rank():
    ranked_resumes = rank_resumes()
    return render_template('rank.html', ranked_resumes=ranked_resumes)

if __name__ == '__main__':
    app.run(debug=True)
