#!/usr/bin/env python
# coding: utf-8

# # AI Powered Resume Ranker and Analyzer
# #### Final Project for AICTE internship on AI: TechSaksham, A Joint CSR initiative of MICROSOFT & SAP.
# ### By Sanju S
# 
# Linkedin: [@Sanju26](https://www.linkedin.com/in/sanju26/)
# 
# Github: [@Sanju26Honey](https://github.com/sanju26honey)
# 
# ---

# #### Import and download required Packages and Libraries

# In[ ]:


import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import pytesseract
from PIL import Image


# In[ ]:


nltk.download('stopwords')
nltk.download('wordnet')


# #### Extract text from PDF Files.
# PDFPlumber was used over PDFReader due to incorrect parsing of spaces by PDFReader

# In[ ]:


import pdfplumber

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# #### Process Text
# The most important part of the project. This is where all the unnecessary stopwords are removed, regex is applied, and lemmatized for further Natural Language Processing

# In[ ]:


def process(text):
    review=re.sub(pattern=r'[^a-zA-Z]', repl=' ', string=text)
    review=review.lower()
    
    review_word=review.split(' ')
    review_word=[word for word in review_word if word not in set(stopwords.words('english'))]
    review_word=[word for word in review_word if len(word) > 3]
    # Remove words which tend to appear in the resume but not in the job description, leading to inaccuracies in ranking
    review_word=[word for word in review_word if word not in ["linkedin","github","objective","summary","references"]]
    # Remove words which tend to appear in the job description but not in the resume, leading to inaccuracies in ranking
    review_word=[word for word in review_word if word not in ["job","canditate","requirements","responsibilities","description","location","date","title"]]
    # Remove months of the year, which usually do not add context
    review_word=[word for word in review_word if word not in ["jan","january","feb","february","mar","march","apr","april","may","jun","june","jul","july","aug","august","sept","september","sep","oct","october","nov","november","dec","december"]]
    review_word=[word.strip() for word in review_word]
    # review_word=[remove_entities(word) for word in review_word]
    # return review
    lemmatizer = WordNetLemmatizer()
    review=[lemmatizer.lemmatize(word, wordnet.VERB) for word in review_word]
    
    review=' '.join(word.strip() for word in review)
    return review


# #### Ranking Resumes

# In[ ]:


# Function to rank resumes based on job description
def rank_resumes(job_description, resumes):
    # Combine job description with resumes
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    # Calculate cosine similarity
    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()
    
    return cosine_similarities


# ### UI
# HTML is used to build the User Interface due to its simplicity. Bootstrap CDN is used for extensive styling.

# In[ ]:


html='''
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>    
<div class="">
<h2 class="title">AI Resume Screening & Analysis System</h2>
<span class="text-muted small">This AI tool scans resumes, ranks them in order, analyzes individual resumes and provides suggestions.</span> 
<br/>
<br/>
<span class="text-muted">Developed by <a href="https://sanju26honey.github.io">Sanju</a></span>
<hr/>
<div class="text-left">
<h4>Step 1: Upload PDF/Image Resumes</h4>
<span class="text-muted">Upload a list of resumes to rank and provide analysis</span>
<br/>
<br/>
'''

st.markdown(html, unsafe_allow_html=True)


# In[ ]:


html='''
<h5>PDF Resume: .pdf</h5>
'''
st.markdown(html, unsafe_allow_html=True)

uploaded_files = st.file_uploader(label="Upload PDF file", label_visibility="collapsed", type=["pdf"], accept_multiple_files=True)


html=f'''
<hr/>
<h4>Step 2: Add Job Description</h4>
'''

st.markdown(html, unsafe_allow_html=True)


# In[ ]:


job_description=st.text_area ("Enter the job description", placeholder="Start typing Job Description here, including requirements and responsibilities...")

html='''
</div>
<hr/>
<h3>Results</h3>
'''

st.markdown(html, unsafe_allow_html=True)


# #### Parse resumes and display Final Results

# In[ ]:


if uploaded_files and job_description:
    
    resume_content = []
    resumes=[]
    job_description=process(job_description)

    # Process each resume
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        resumes.append(text)
        text=process(text)
        
        # Check only for words of resume that are present in the job description. This is because the resume can also contain details about various projects, such as name of the project and implemeentation information, which may not be present in the job description, leading to inaccuracies in ranking.
        text=[word for word in text.split(' ') if word in job_description.split(' ')]
        resume_content.append(' '.join(text))
    
    # Rank resumes
    scores = rank_resumes(job_description, resume_content)

    results=[]

    # Make a list of format [file_name, file_content, resume_content, score]
    # Where resume_content: processed file_content
    
    for i in range(len(resumes)):
        results.append([uploaded_files[i].name, extract_text_from_pdf(uploaded_files[i]), resume_content[i], round(scores[i]*100, 2)])

    # Sort results by score
    results.sort(key=lambda x:x[3], reverse=True)

    # Format and display results 
    table="<table>"
    table+="""
    <thead>
        <tr>
            <th></th>
            <th>File Name</th>
            <th>Score</th>
        </tr>
    </thead>
    """

    table+="<tbody>"
    i=1
    for file_name, fc, content, score in results:
        table+=f"<tr><td>{i}</td><td>{file_name}</td><td>{score}%</td></tr>"
        i+=1
    
    table+="</tbody>"
    table+="</table>"

    st.markdown(table, unsafe_allow_html=True)

    # Individually Analyze each resume
    st.subheader("Individual Analysis")
    for file_name, file_content, content, score in results:
        html_str=f"<h4>{file_name}</h4>"
        html_str+=f"<h5>Score: {score}%</h5>"

        # Code for progress bar
        
        html_str += f"""
        <div class="progress" role="progressbar" aria-label="Warning example" aria-valuenow="{score}" aria-valuemin="0" aria-valuemax="100">
        <div class="progress-bar bg-success" style="width:{score}%; color: white">{score}%</div>
        </div>
        <br/>
        <p class="text-muted">Add Missing Keywords given in the 'Missing Keywords' section to enhance your score</p>
        """
        st.markdown(html_str, unsafe_allow_html=True)

        # Highlighted Analysis
        html='''
        <h4>Outcome:</h4>
        <p class="text-muted">Highlighted words are keywords from job description that are included in the resume</p>
        <div>'''
        file_content = file_content.replace('\n', '<br>')
        
        for word in file_content.split(' '):
            w=process(word)
            if w in job_description.split(' ') and w in content.split(' '):
                html+=f'<mark class="px-2" style="background:rgba(104, 251, 170, 0.7)">{word}</mark> '
            else:
                html+=f'<span>{word}</span> '
        html+='</div>'
        html+='<div>'
        
        st.markdown(html, unsafe_allow_html=True)

        # Display WordCloud
        wordcloud = WordCloud(background_color=None, mode='RGBA', colormap='Greens', scale=2, width=750).generate(resumes[0])

        st.subheader('Word Cloud Analysis')

        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        ax.imshow(wordcloud, interpolation='bilinear')

        ax.axis('off')

        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.margins(0)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
        buf.seek(0)
        
        st.image(buf)
        html='</div>'

        # Display Missing Keywords
        st.subheader('Missing Keywords')
        html+='<div class="row px-3">'
        for word in set(job_description.split(' ')):
            if word not in content.split(' '):
                html+=f'<span class="col px-3 m-1" style="border: 1px solid #ccc;">{word}</span> '
        html+='</div><hr/>'
        
        st.markdown(html, unsafe_allow_html=True)

