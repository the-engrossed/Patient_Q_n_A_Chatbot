from setuptools import setup, find_packages

setup(
    name="patient_qna_chatbot",
    version="0.1",
    description="A patient Q&A chatbot using LangChain, OpenAI, and Streamlit.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
        "streamlit","pandas", "langchain_core","langchain_community", "chromadb"
    ],
    python_requires=">=3.8",
)