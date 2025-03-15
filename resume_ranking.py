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


st.set_page_config(layout="wide")


html='''
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/5.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<style>
    html,body,#stMarkdownContainer {
        height: 100% !important;
        width: 100% !important
    }
    .stMainBlockContainer  {
        padding:0;
        margin:0;
    }
    .page {
        height: 100vh !important;
    }
    .st-key-container {
        padding:10%;
        overflow:hidden;
        width:100% !important;
    }
    .stMarkdown, .stElementContainer {
        max-width:100% !important;
    }
    .stFileUploader, .st-key-element2 {
        max-width: 75% !important;
    }
    .stTextArea {
        max-width:100%;
    }
</style>    
<div class="px-4 py-5 w-100 text-left d-flex align-items-center page">
    <div>
        <div class="col-lg-9 mx-auto">
            <h1 class="display-3 fw-bold">Resume Ranker and Analyzer</h1>
            <p class="lead mb-4">The ultimate tool to revolutionize hiring workflows. This Resume Analyzer streamlines the recruitment process by leveraging cutting-edge technology to rank resumes, visualize key insights, and identify skill gaps—all in just a few clicks. Experience the future of talent acquisition, designed to make your decisions smarter and faster.</p>
            <div class="">
            <span class="lead">Developed with ❤️ by <a href="https://sanju26honey.github.io" class="text-decoration-none">Sanju</a><br/><br/>
            <a href="#step-1-upload-resumes" class="btn me-3 p-3 px-5 text-decoration-none text-white" style="background: #019161">Get Started</a><a href="#Page2" class="btn me-3 p-3 px-5 btn-dark text-decoration-none text-white">Know More</a>
            </div>
            <!-- <p class="text-muted">Scroll to know more</p> -->
        </div>
    </div>
</div>
<div class="px-4 py-5 my-5 text-left d-flex align-items-center page" id="Page2">
    <div>
        <div class="col-lg-10 mx-auto">
            <h1 class="">Features</h1>
            <br>
            <div class="row">
                <div class="feature col text-justify">
                    <div>
                        <h2>🥇 Rank Resumes</h2>
                        <p>Leverage advanced NLP algorithms to rank resumes based on their alignment with job descriptions, ensuring the most suitable candidates are prioritized.</p>
                    </div>
                </div>
                <div class="feature col text-justify">
                    <div>
                        <h2>🔎 Keyword Analysis</h2>
                        <p>Identify and highlight critical keywords to evaluate resume relevance, detect missing skills, and provide actionable insights for recruiters.</p>
                    </div>
                </div>
                <div class="feature col text-justify">
                    <div>
                        <h2>🥇 Wordcloud Analysis</h2>
                        <p>Visualize key strengths and skills with personalized word clouds, offering a quick and intuitive way to analyze each candidate's profile.</p>
                    </div>
                </div>
                </div>
        </div>
    </div>
</div>
<div class="px-4 py-5 my-5 text-left d-flex align-items-center page">
    <div>
        <div class="col-lg-10 mx-auto">
            <h1 class="">Tech Stack</h1>
            <br>
            <div class="row">
                <div class="feature col text-justify m-1">
                    <h3 class="font-monospace">🛠️ Python</h3>
                    <p class="small">Chosen for its versatility and vast libraries, making it ideal for NLP and data-driven tasks.</p>
                </div>
                <div class="feature col text-justify m-1">
                    <h3 class="font-monospace">🧠 NLP</h3>
                    <p class="small">Processes and analyzes textual data, removes stopwords, and lemmatized data to extract meaningful insights and enhance resume analysis.</p>
                </div>
                <div class="feature col text-justif m-1y">
                    <h3 class="font-monospace">🤖 SKLearn</h3>
                    <p class="small">Provides robust tools for implementing TF-IDF and cosine similarity for precise ranking.</p>
                </div>
            </div>
            <div class="row">
                <div class="col m-1">
                    <h3 class="font-monospace">📒 Jupyter</h3>
                    <p class="small">Facilitates iterative development and easy visualization of data analysis and modeling.</p>
                </div>
                <div class="col m-1">
                    <h3 class="font-monospace">🧑‍🔧 PDFPlumber</h3>
                    <p class="small">Efficiently extracts text from PDF resumes, ensuring accurate content processing.</p>
                </div>
                <div class="col m-1">
                    <h3 class="font-monospace">🎨 HTML + Bootstrap</h3>
                    <p class="small">Combines HTML's structure with Bootstrap's responsive and pre-styled components to create a modern, user-friendly interface effortlessly.</p>
                </div>
            </div>
            <div class="row">
                <div class="col m-1">
                    <h3 class="font-monospace">🖌️ Streamlit</h3>
                    <p class="small">Simplifies the creation of an interactive, user-friendly web interface for the application.</p>
                </div>
                <div class="col m-1">
                    <h3 class="font-monospace">🐼 Pandas & Numpy</h3>
                    <p class="small">Offers powerful tools for data manipulation, cleaning, and efficient numerical computations.</p>
                </div>
                <div class="col m-1">
                    <h3 class="font-monospace">📈 Plotly & Wordcloud</h3>
                    <p class="small">Creates interactive charts and visual word clouds to enhance the analysis and user experience.</p>
                </div>
            </div>
        </div>
    </div>
</div>
'''

st.markdown(html, unsafe_allow_html=True)


# In[ ]:


with st.container(key="container"):
    html='''
    <div id="Page3"></div>
    <h2 class="">Step 1: Upload Resumes</h2>
    <span class="text-muted">Upload a list of resumes to rank and provide analysis</span>
    '''
    st.markdown(html,unsafe_allow_html=True)
    uploaded_files = st.file_uploader(label="Upload PDF file", key="element1", label_visibility="collapsed", type=["pdf"], accept_multiple_files=True)


    html=f'''
            <hr/>
            <h2>Step 2: Add Job Description</h2>
    '''

    st.markdown(html, unsafe_allow_html=True)
    

    job_description=st.text_area ("Enter the job description", key="element2", placeholder="Start typing Job Description here, including requirements and responsibilities...")

    html='''
        </div>
        <hr/>
        <h1>Results</h1>
    '''

    st.markdown(html, unsafe_allow_html=True)
    # #### Parse resumes and display Final Results
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
            
            st.markdown(html, unsafe_allow_html=True)

    html='''</div><hr/></div></div>
    <div class="footer">
    <span class="lead">Developed with ❤️ by <a href="https://sanju26honey.github.io" class="text-decoration-none">Sanju</a><br/>
    <span class="text-muted">&copy 2025 Resume Ranker & Analyzer. All Rights Reserved</span>
    </div>
    </div>'''
    
    st.markdown(html, unsafe_allow_html=True)


