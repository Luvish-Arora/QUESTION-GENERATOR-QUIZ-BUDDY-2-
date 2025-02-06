# Question Generator - Quiz Buddy 2

## 📌 Project Overview
**Question Generator - Quiz Buddy 2** is an AI-powered quiz generation tool that extracts content from **user-uploaded PDFs** to create **personalized quizzes**. The system uses **Flask** for the backend, **JavaScript** for interactivity, and **Excel** for storing generated questions.

## 🚀 Features
- **Upload PDFs** and generate quiz questions automatically
- **Randomized Question Selection** to ensure variety
- **Excel Integration** to store and retrieve questions
- **REST API** to fetch quiz questions dynamically
- **JavaScript-powered quiz interface** for an interactive experience

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Libraries:** pandas, openpyxl, werkzeug, random, logging
- **Database:** Excel file (generated_questions.xlsx) for storing quiz data

## 🔧 Installation & Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Luvish-Arora/QUESTION-GENERATOR-QUIZ-BUDDY-2-.git
   cd QUESTION-GENERATOR-QUIZ-BUDDY-2-
   ```
2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application:**
   ```bash
   python main.py
   ```
5. **Access the Application:**
   - Open [http://localhost:5000](http://localhost:5000) in your browser.

## 📂 Project Structure
```
QUESTION-GENERATOR-QUIZ-BUDDY-2/
│── static/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│── templates/
│   ├── index.html         # Upload page
│   ├── quiz.html          # Quiz interface
│   ├── quiz_complete.html # Displayed when all questions are used
│── uploads/               # Stores uploaded PDFs
│── .gitignore
│── QuizGenerator.py       # Handles PDF processing and question generation
│── app.py                 # Flask backend
│── generated_questions.xlsx  # Stores generated quiz questions
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```



