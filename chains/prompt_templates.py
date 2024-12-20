from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# System prompt for your medical QA assistant  
SYSTEM_MESSAGE = """
You are a trustworthy medical Q&A assistant.  
Answer questions using only the provided context below.  
If the information is not present or insufficient, reply:  
"Sorry, I cannot answer based on the available data."
Add a disclaimer: Always consult a healthcare professional.
Context:
{context}
"""

# ChatPromptTemplate for RAG chain (for use with ChatOpenAI)
rag_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),
    ("human", "{input}")   # inserts user's actual question
])

# Optional: Simple PromptTemplate for summarization tasks
summary_prompt = PromptTemplate(
    template="Summarize the following medical context for a layperson:\n{text}",
    input_variables=["text"]
)

# Optional: Prompt for safety/disclaimer messages
disclaimer_prompt = PromptTemplate(
    template="Important: This answer is informational only. Always consult a healthcare provider.",
    input_variables=[]
)

faq_prompt = PromptTemplate(
    template=(
        "Based on the following medical context, write 3-5 Frequently Asked Questions (FAQs) and answers. "
        "Format them as clearly separated Q&A pairs for a patient-friendly chatbot.\n"
        "Context:\n{context}\n\n"
        "FAQ:"
    ),
    input_variables=["context"]
)


# For compatibility, export the main templates
__all__ = ["rag_chat_prompt", "summary_prompt", "disclaimer_prompt", "faq_prompt"]
