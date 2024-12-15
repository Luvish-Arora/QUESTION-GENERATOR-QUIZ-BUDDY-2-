from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pandas as pd
from werkzeug.utils import secure_filename
from QuizGenerator import QuizGenerator  # Import your quiz generation class and methods
import logging
import random

# Initialize the Flask application
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store questions and used question IDs
questions = []

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to load questions from Excel
def load_questions():
    global questions
    if os.path.exists('generated_questions.xlsx'):
        df = pd.read_excel('generated_questions.xlsx')
        questions = df.to_dict(orient='records')
    else:
        questions = []

# Function to save questions to Excel
def save_to_excel(questions):
    df = pd.DataFrame(questions)
    if 'used' not in df.columns:
        df['used'] = False  # Ensure 'used' column exists
    df.to_excel('generated_questions.xlsx', index=False)

@app.route('/')
def index():
    """Render the homepage where users can upload PDFs."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF file uploads and generate questions."""
    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')
    
    # Handle multiple file uploads
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Initialize the quiz generator
            quiz_gen = QuizGenerator()
            
            # Process the uploaded PDF and generate questions
            raw_questions = quiz_gen.process_pdf(filepath)
            
            # Prepare questions with separated options
            processed_questions = []
            for question in raw_questions:
                options = question.get('options', [])
                if isinstance(options, str):
                    options = options.split(';')  # Change delimiter if needed

                processed_questions.append({
                    'id': len(processed_questions) + 1,
                    'question': question.get('question', ''),
                    'context': question.get('context', ''),
                    'option1': options[0] if len(options) > 0 else '',
                    'option2': options[1] if len(options) > 1 else '',
                    'correct_answer': question.get('correct_answer', ''),
                    'used': False
                })
            
            # Save the processed questions to the Excel file
            if processed_questions:
                save_to_excel(processed_questions)
                logger.info("Questions saved to 'generated_questions.xlsx'")
            else:
                logger.warning("No questions were generated!")

    # Load questions after processing
    load_questions()

    # Redirect to the quiz page after processing
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    """Render the quiz page with a random question."""
    if not questions:
        return render_template('quiz_complete.html')  # Render a page when all questions are used

    # Filter unused questions
    unused_questions = [q for q in questions if not q['used']]

    if not unused_questions:
        return render_template('quiz_complete.html')  # Render a page when all questions are used

    # Randomly pick an unused question
    question = random.choice(unused_questions)
    question['used'] = True  # Mark question as used
    save_to_excel(questions)  # Save updated questions to Excel

    return render_template('quiz.html', question=question)

@app.route('/get-random-question')
def get_random_question():
    """API endpoint to get a random question."""
    unused_questions = [q for q in questions if not q['used']]

    if unused_questions:
        question = random.choice(unused_questions)
        question['used'] = True  # Mark question as used
        save_to_excel(questions)  # Save updated questions to Excel
        return jsonify(
            question=question['question'],
            context=question.get('context', ''),
            option1=question['option1'],
            option2=question['option2']
        )
    else:
        return jsonify(message="All questions have been used!")

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Load questions at the start
    load_questions()
    app.run(debug=True)
