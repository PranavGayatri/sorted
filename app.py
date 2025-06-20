from flask import Flask, render_template, request, redirect, send_file
import os
import pandas as pd
from parser.extractor import parse_resume
from email_fetcher import fetch_resumes
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        app_password = request.form['app_password']
        required_skills = [s.strip() for s in request.form['skills'].split(',') if s.strip()]
        min_experience = int(request.form['min_experience'])
        location_pref = request.form['location']

        if 'fetch' in request.form:
            fetch_resumes(email, app_password)

        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filepath)

        resumes = [os.path.join(UPLOAD_FOLDER, r) for r in os.listdir(UPLOAD_FOLDER) if r.endswith(('.pdf', '.docx'))]
        data = []
        for resume in resumes:
            parsed = parse_resume(resume, required_skills)
            parsed['Skill Match'] = len(parsed['Skills'])
            parsed['Pass'] = parsed['Experience'] >= min_experience and (location_pref.lower() in parsed['Location'].lower() if location_pref else True)
            data.append(parsed)

        df = pd.DataFrame(data)
        df = df.sort_values(by=['Pass', 'Skill Match', 'Experience'], ascending=False)
        df.to_csv('parsed_data/filtered_candidates.csv', index=False)
        return render_template('index.html', candidates=df.to_dict(orient='records'), show_results=True)

    return render_template('index.html', candidates=[], show_results=False)

@app.route('/download')
def download():
    return send_file('parsed_data/filtered_candidates.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
