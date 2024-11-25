import streamlit as st
import PyPDF2
import requests
import os
from main import stream


db = "data"
if not os.path.exists(db):
    os.makedirs(db)
st.title("chat resume")


with st.sidebar:
   
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
       
        st.write("added")
        content = ""
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in range(len(pdf_reader.pages)):
            print(page)
            content += pdf_reader.pages[page].extract_text()
            # Display the content
        st.write(content)
        pdf_path = os.path.join(db,"res.pdf")
        with open(pdf_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        # button = st.button("click")
        # if uploaded_file and button:
        #     url2 = "https://8000-01j9tsgnt0d94299yeq925m6yg.cloudspaces.litng.ai/resume"
            
            # with open(pdf_path, "rb") as pdf_file:
            #     files = {"file": ("resume.pdf", pdf_file, "application/pdf")}
            #     response = requests.post(url2, files=files)
            # response = response.json()              
            # print(response)
            # st.write(response)
  
  
prompt = st.chat_input("Say something")
if prompt:
    response = stream({"input":prompt})
    st.write_stream(response)

    # response = stream({"input":prompt})
    # for res in response:
    #     print(res,end="",flush = True)
    #     st.write(f"User has sent the following prompt: {prompt}")  
  
            
# resume = st.file_uploader("upload")
# if resume:
#     content = resume.getvalue()
#     post_url = "https://8000-01j9tsgnt0d94299yeq925m6yg.cloudspaces.litng.ai/resume"
#     pdf_content = resume.read()
    
#     files = {"file": (resume.name, pdf_content, "application/pdf")}
#     response = requests.post(post_url, files=files)
#     response = response.json()
#     st.write(response)
    
            