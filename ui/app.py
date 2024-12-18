import streamlit as st
from chains.rag_chain import load_vectordb, build_qa_chain
from chains.prompt_templates import faq_prompt
from langchain_openai import ChatOpenAI
import re
from utils.safety import needs_urgent_escalation, is_sensitive_topic, append_disclaimer, redact_sensitive_info

st.title("Patient Q&A Chatbot")

# Use st.form so "Enter" triggers the answer
with st.form("question_form"):
    user_question = st.text_input("Ask a medical question:")
    submitted = st.form_submit_button("Get Answer")

if submitted and user_question:
    vectordb = load_vectordb()
    qa_chain = build_qa_chain(vectordb)
    result = qa_chain.invoke({"input": user_question})

    st.subheader("Answer")
    st.write(result['answer'])

    st.subheader("Relevant Sources")
    for doc in result['context']:
        with st.expander(f"Question: {doc.metadata.get('question', 'Relevant Source')}"):
            st.write(doc.page_content)
            

    st.subheader("Frequently Asked Questions")
    combined_context = "\n".join([doc.page_content for doc in result['context']])
    llm = ChatOpenAI(model="gpt-4-turbo")
    faq_prompt_text = faq_prompt.format(context=combined_context)
    faqs = llm.invoke(faq_prompt_text)

    faq_text = faqs.content if hasattr(faqs, "content") else str(faqs)
    pairs = re.findall(r'\*\*Q: (.*?)\*\*\s*A: (.*?)(?=\n\s*\*\*Q:|\Z)', faq_text, re.DOTALL)
    if pairs:
        for question, answer in pairs:
            st.markdown(f"**Q: {question.strip()}**")
            st.markdown(f"A: {answer.strip()}")
            st.markdown("---")
    else:
        st.write(faq_text)
