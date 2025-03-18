# AI powered Resume Ranking and Analysis system
### Live Demo: [resumerankerandanalyzer.streamlit.app](https://resumerankerandanalyzer.streamlit.app/)
(You can use resumes and job description given in Samples folder)

### Developed by [Sanju](https://sanju26honey.github.io) as a Final Project for AICTE internship on AI: TechSaksham, A Joint CSR initiative of MICROSOFT & SAP.

### Let's Connect:

Linkedin: [@Sanju26](https://www.linkedin.com/in/sanju26/)

Github: [@Sanju26Honey](https://github.com/sanju26honey)

---
## About this project

This project uses Natural Language Processing to analyze resumes, match them with a given Job Description and rank them accordingly.

## Usecase

This can be used by both Recruiters and applicants alike. Recruiters can use this to rank resumes based on the given job description. While Applicants can use this to analyze their resumes, find missing keywords and wordcloud analysis.

---

## Features

- **Automated Resume Screening**: Processes and ranks resumes based on their relevance to a job description, saving recruiters time and effort.
- **TF-IDF Feature Extraction**: Extracts meaningful features from resumes and job descriptions for accurate matching.
- **Cosine Similarity Matching**: Computes similarity scores to rank resumes by their fit with job requirements.
- **Top Resume Ranking**: Provides a ranked list of the top 10 most relevant resumes for easy review.
- **Bias Mitigation**: Integrates fairness constraints to ensure unbiased evaluations.
- **User-Friendly Interface**: Designed with a seamless and intuitive interface for easy interaction.
- **Scalable Architecture**: Handles large volumes of resumes efficiently, suitable for enterprise use.
- **Integration Ready**: APIs available for integration with applicant tracking systems (ATS) or other HR tools.

---

## Tech Stack

### Programming Languages:
- **Python 3.8+**

### Libraries and Frameworks:
- **NLP**: Scikit-learn, NLTK
- **Feature Extraction & Similarity**: TF-IDF, Cosine Similarity
- **Web Interface**: Flask
- **Data Manipulation**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn

### Tools:
- **Resume Parsing**: PDFPlumber for reading and extracting text from PDF resumes.
- **Deployment**: Deployed using Streamlit.

---

## How It Works

1. **Resume Parsing**: Extracts text from resumes in PDF format and preprocesses the data.
2. **Feature Extraction**: Employs TF-IDF to identify key features in resumes and job descriptions.
3. **Similarity Matching**: Uses Cosine Similarity to compute relevance scores for each resume.
4. **Ranking**: Implements the K-Nearest Neighbors (KNN) algorithm to rank the top 10 resumes.
5. **Output Results & Individual Analysis**: Individually Analyze each resume with highlighted keywords, wordcloud analysis, and missing keyword analysis.

---

## Future Work

- Explore advanced models like BERT for improved semantic understanding (optional).
- Incorporate additional fairness metrics and dynamic weighting customization.
- Expand the system for multi-language support to cater to global recruitment needs.
- Integrate explainability tools like LIME or SHAP to enhance recruiter trust.

---

## Installation
To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/sanju26honey/resume_ranking.git
    cd resume_ranking
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    streamlit run resume_ranking.py
    ```

---

## Screenshots

![image](https://github.com/user-attachments/assets/046e3b63-f407-46d0-a07a-1a3537691c0d)
![image](https://github.com/user-attachments/assets/c9e40699-78f9-4d0f-97b2-cdc813f83d05)
![image](https://github.com/user-attachments/assets/94cb5816-ed97-42d4-a0ef-07ba526a8569)
![image](https://github.com/user-attachments/assets/806dbdd2-0b50-40d0-93cf-3e67459fdd63)
![image](https://github.com/user-attachments/assets/679de8ac-473e-4cd8-a9e4-fa77cf438210)
![image](https://github.com/user-attachments/assets/fda0f6ae-fca3-4f63-9591-35a7be77dae5)
![image](https://github.com/user-attachments/assets/231ffc9f-5325-4573-b17e-325b62e75354)
