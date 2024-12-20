from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from chains.prompt_templates import rag_chat_prompt, faq_prompt
from retrieval.vectordb import get_openai_embeddings
from retrieval.loader import load_medquad, df_to_documents
from dotenv import load_dotenv

load_dotenv()

def load_vectordb(persist_directory="db/chroma/"):
    embeddings = get_openai_embeddings()
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )


def build_qa_chain(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})  # Retrieve top 5 relevant docs
    llm = ChatOpenAI(model="gpt-4-turbo")
    # This step replaces the old PromptTemplate & chain
    document_chain = create_stuff_documents_chain(llm, rag_chat_prompt)
    # Use the new retrieval chain constructor
    qa_chain = create_retrieval_chain(retriever, document_chain)
    return qa_chain

if __name__ == "__main__":
    vectordb = load_vectordb()
    qa_chain = build_qa_chain(vectordb)
    question = "What are the symptoms of diabetes?"
    result = qa_chain.invoke({"input": question})
    print(f"Question: {question}")
    print(f"Answer: {result['answer']}\n")
    print("Relevant sources:")
    combined_context = "\n".join([doc.page_content for doc in result['context']])
    for doc in result['context']:
        print(doc.page_content[:200], '...')

    # ---- FAQ generation ----
    print("\nFrequently Asked Questions:")
    llm = ChatOpenAI(model="gpt-4-turbo")
    faq_prompt_text = faq_prompt.format(context=combined_context)
    faqs = llm.invoke(faq_prompt_text)
    print(faqs)    
