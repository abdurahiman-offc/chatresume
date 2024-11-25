import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import JinaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

groq_api = "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"
text_embeddings = JinaEmbeddings(
    jina_api_key="jina_45295d61209a42d8ac3b864b6e447c6eVEiiku_KyB3ZKKnm3PSjx1MXMLLC", model_name="jina-embeddings-v2-base-en"
)

def load_llm():
    llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    groq_api_key = groq_api,
    streaming = True
    )
    return llm



def load_chat_prompt():
    system_prompt = ("You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}")
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
    )
    return prompt

def load_retriever():
    pdf_path = os.path.join("data","res.pdf")
    print(pdf_path)
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    # print(f"{pages[0].metadata}\n")
    # print(pages[0].page_content)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
    splits = text_splitter.split_documents(pages)
    vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=text_embeddings
        )

    retriever = vectorstore.as_retriever()
    return retriever
    
def qa():
    llm = load_llm()
    prompt = load_chat_prompt()
    retriever = load_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain

# chat = qa()
# chat.invoke({"prompt":"get the name, email and contact details"})

# vect = load_retriever()
# res =vect.invoke("skills")
# for page in res:
#     print(page.page_content)
    
def stream(prompt):
    import time
    ai = qa()
    stream_out = ai.stream(prompt)
    for chunk in stream_out:
        yield chunk.get("answer")
        time.sleep(0.3)

# response = stream({"input":"get the name, email and contact from the resume"})
# for res in response:
#     print(res,end="",flush = True)
    
