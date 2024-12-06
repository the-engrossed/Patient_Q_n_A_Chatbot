from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from retrieval.vectordb import get_openai_embeddings
from dotenv import load_dotenv

load_dotenv()

def load_vectordb(persist_directory="db/chroma/"):
    embeddings = get_openai_embeddings()
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

prompt_template = PromptTemplate(
    template="""
You are a medical QA assistant. Use only the given source info.
If the info is not enough, say: "Sorry, I cannot answer based on the available data."

{context}

Question: {question}
Answer:""",
    input_variables=["context", "question"]
)

def build_qa_chain(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})  # Retrieve top 5 relevant docs
    llm = ChatOpenAI(model="gpt-4-turbo")  
    qa = RetrievalQA(
        retriever=retriever,
        llm=llm,
        prompt_template=prompt_template,
        return_source_documents=True
    )
    return qa

if __name__ == "__main__":
    vectordb = load_vectordb()
    qa_chain = build_qa_chain(vectordb)
    question = "What are the symptoms of diabetes?"
    result = qa_chain({"question": question})
    print(f"Question: {question}")
    print(f"Answer: {result['result']}\n")
    print("Relevant sources:")
    for doc in result['source_documents']:
        print(doc.page_content[:200], '...')
