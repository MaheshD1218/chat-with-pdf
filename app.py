import streamlit as st
import pickle 
from dotenv import load_dotenv
from  PyPDF2 import PdfReader 
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Sidebar Contents
with st.sidebar:
    st.title("Chat With Pdf")
    st.markdown(
        '''
        ##About
       This app is an LLM powered chatbot built using :
       - [Streamlit](https://streamlit.io/)        
       - [LangChain](https://python.langchain.com/)        
       - [OpenAi](https://platform.openaicom/docs/models)        
        
    ''')
    add_vertical_space(5)
    st.write("Made by Mahesh by following a reference video uploaded on youtube")
    
def main():
        st.header("Chat with PDF")
        
        load_dotenv()
        
        # upload a pdf 
        pdf = st.file_uploader("Upload your PDF file" , type="pdf")

        # st.write(pdf)

        pdf_reader=PdfReader(pdf);
     
        text = ""
        if pdf_reader is not None:
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # st.write(text)
        
        
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            
            )
        
        chunks = text_splitter.split_text(text=text)
        
        # st.write(chunks)
        
        # Embeddings 
        store_name=pdf.name[:-4]

        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        VectoreStores = FAISS.from_texts(chunks,embeddings)
        with open(f"{store_name}.pkl","wb") as f :
            pickle.dump(VectoreStores,f)

        # Questions
        query = st.text_input("Ask Questions about your pdf file")  
        # st.write(query)


        if query :
            docs = VectoreStores.similarity_search(query,k=3)
            st.write(docs)

        
        model_name = "deepset/roberta-base-squad2"
        
        # a) Get predictions
        nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
        QA_input = {
            'question': query,
            'context': docs[0]
        }
        res = nlp(QA_input)
        
        st.write(res['answer'])

                
if __name__ == '__main__':
    main()