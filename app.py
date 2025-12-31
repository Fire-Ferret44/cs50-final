"""
This is my flask application file for the web demo
"""
from io import BytesIO
import os
import re
from pathlib import Path

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, session, redirect, send_file, url_for

from main import run_scheduler_from_paths
from utility.flask_utils import apology
from utility.file_parser_utils import validate_if_csv, validate_headings
from utility.filereader_utils import get_next_upload_file_number

load_dotenv()

# Configure flask application
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
@app.route('/index')
# Index/Home page
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
# Page to upload files for scheduler
def create():
    """Render the create page and handle file uploads."""
    if request.method == "POST":

        uploaded_files = {
        "doctors": request.files.get("doctors"),
        "leave": request.files.get("leave"),
        "pairing_constraints": request.files.get("pairing_constraints"),
        "schedule_period": request.files.get("schedule_period"),
        "shift_structure": request.files.get("shift_structure")
        }

        required_files = [
            "doctors",
            "leave",
            "pairing_constraints",
            "schedule_period",
            "shift_structure",
        ]

        missing = [k for k in required_files if not uploaded_files.get(k)]
        if missing:
            message=f"Missing required files: {', '.join(missing)}"
            return render_template('apology.html', message=message, code=400)
            # if one of the above files are missing issue an apology

        valid_files = []
        # Check if uploaded files are csv and correct headings
        for key, value in uploaded_files.items():
            if not value:
                continue
            if not validate_if_csv(value):
                message= f"{key} file is not a valid CSV file"
                return render_template('apology.html', message=message, code=400)
            valid, message = validate_headings(value, key)
            if not valid:
                return render_template('apology.html', message=message, code=400)
            valid_files.append(key)

        file_number = get_next_upload_file_number(Path("data/user_input"))
        session["file_number"] = file_number  # Store file number in session

        #Save files after validation
        for key, value in uploaded_files.items():
            if value:
                file_path = os.path.join("data/user_input", f"{key}_{file_number}.csv")
                # Users cannot name files
                value.seek(0)
                value.save(file_path)

        flash(f"The following files were uploaded and validated: {', '.join(valid_files)}")
        # Render a generate.html page that says which files were validated successfully
        return redirect(url_for('generate'))

    # for when method is get:
    return render_template('create.html')

@app.route('/generate', methods=['GET','POST'])
# Page to run the scheduler
def generate():
    """Generate the schedule based on uploaded files."""
    if request.method == 'POST':
        print("Generate button pressed")
        print(session.get("file_number"))
        input_path = Path("data/user_input")
        #output_dir = Path("tests/output/user_output")

        file_number = session.get("file_number")
        if not file_number:
            return apology("Missing session information for file number", code=400)

        # Check if all required files are present
        rostered_scheduler = run_scheduler_from_paths(input_path, file_number)

        session['schedule_text'] = rostered_scheduler["schedule_text"]
        session['metadata_text'] = rostered_scheduler["metadata_text"]

        return redirect('/result')

    else:
        return render_template('generate.html')

@app.route('/result', methods=['GET'])
# Page to display the result of the scheduler
def result():
    """Display the result of the scheduler."""
    if 'schedule_text' not in session or 'metadata_text' not in session:
        return apology("No schedule data available", code=400)

    schedule_text = session['schedule_text']
    metadata_text = session['metadata_text']

    return render_template('result.html', schedule_text=schedule_text, metadata_text=metadata_text)
    # Display the schedule and metadata in a formatted way

def strip_html_tags(text: str) -> str:
    """Remove HTML tags for plain text output."""
    return re.sub(r"<[^>]+>", "", text)

@app.route('/download', methods=['GET'])
# Endpoint to download the schedule and metadata as text files
def download():
    """Download the schedule and metadata as a text file."""
    if 'schedule_text' not in session or 'metadata_text' not in session:
        return apology("No schedule data available for download", code=400)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    schedule_text = strip_html_tags(session['schedule_text'])
    metadata_text = session['metadata_text']

    # Create a temporary file to hold the combined output
    file_content = (
    f"Generated on: {timestamp}\n\n"
    "===Roster Schedule===\n\n"
    f"{schedule_text}\n\n"
    "===Metadata===\n\n"
    f"{metadata_text}\n"
    )

    buffer = BytesIO()
    buffer.write(file_content.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='roster.txt',
        mimetype='text/plain'
    )

@app.route('/apology', methods=['GET'])
# Apology page for errors
def apology_page():
    """Render the apology page."""
    message = request.args.get('message', 'An error occurred')
    code = request.args.get('code', 400)
    return render_template('apology.html', message=message, code=code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
