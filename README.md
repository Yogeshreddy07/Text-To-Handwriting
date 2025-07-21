
# ✍️ Text2Ink — Text to Handwriting Converter + AI Assistant

**Text2Ink** is a web application that transforms digital text into visually appealing handwritten documents and includes an AI-powered assistant to help users learn and explore topics like AI ,ML and All the topics.  
Built using **HTML, CSS, JavaScript, Django, Python**, and integrated with **OpenAI (Ollama)** and **DeepSeekAI** for AI chat features.

---

## 🌟 Features

### 🖋️ Text to Handwriting Generator
- Type or paste your text
- Choose from **multiple handwriting fonts**
- Customize:
  - **Backgrounds** (e.g. ruled, plain)
  - **Text color**
- **Generate PDF** output that mimics real handwriting

### 🤖 AI-Powered Smart Assistant
- Ask any AI-related or educational question
- Uses **OpenAI** + **DeepSeekAI** to provide in-depth responses
- Ideal for students and curious learners

---

## 🖼️ Preview

### ✅ Homepage  
> “Transform your text into realistic handwriting”  
Includes reasons to choose Text2Ink: styles, wrapping, and usability.

### ✍️ Generator Page  
> Enter text → Select font/background/color → Generate PDF

### 🤖 Learn With AI  
> Ask questions in natural language and get detailed AI-generated responses.

---

## 🛠️ Tech Stack

| Frontend | Backend | AI Integration | Output |
|---------|---------|----------------|--------|
| HTML, CSS, JS | Django (Python) | Ollama, DeepSeekAI | PDF Generation |

---

## 🧪 How It Works

### Text-to-Handwriting Flow:
1. User enters text into a textarea
2. Chooses handwriting style, background, and color
3. Backend uses **Python & libraries like FPDF / PIL** to generate a realistic handwritten **PDF**
4. PDF is returned as downloadable output

### AI Assistant Flow:
1. User types a question (e.g., "What is AI?")
2. The question is sent to **DeepSeekAI or OpenAI (via Ollama)**
3. Model processes and returns informative, structured answers
4. Results are displayed in real time

---

## 🚀 Installation Guide

```bash
# Clone the repository
git clone https://github.com/Yogeshreddy07/Text2Ink.git
cd Text2Ink

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt

# Run the server
python manage.py runserver
```

---

## 📁 Folder Structure

```
Text2Ink/
├── templates/
│   ├── index.html
│   ├── generator.html
│   └── ai_assistant.html
├── static/
│   ├── css/
│   ├── js/
├── core/
│   ├── views.py
│   ├── forms.py
│   └── utils/
│       └── pdf_generator.py
├── ai/
│   └── chat_engine.py  # integrates OpenAI/DeepSeek
```

---

## 📦 Dependencies

- Django
- Pillow (for image/font handling)
- FPDF or ReportLab (for PDF generation)
- Ollama / OpenAI SDK
- DeepSeekAI integration

---

## 📄 License

This project is open-source and intended for **learning**, **sharing**, and **growth**.  
Feel free to fork, build on it, and give credit where due. 🙏

> “The beautiful thing about learning is that nobody can take it away from you.”  
> — *B.B. King*

---

## 🙌 Let's Connect

📧 Email: yogeshreddys07@gmail.com  
💼 LinkedIn: [linkedin.com/in/yogeshreddy07](https://linkedin.com/in/yogeshreddy07)  
🐱 GitHub: [github.com/Yogeshreddy07](https://github.com/Yogeshreddy07)
