import pandas as pd
from langchain_core.documents import Document

def load_medquad(path="data/medquad_clean.csv"):
    """Loads MedQuAD medical Q&A CSV and returns a cleaned DataFrame."""
    df = pd.read_csv(path)
    # Basic cleaning: Drop rows with missing Q/A, strip whitespace
    df = df.dropna(subset=["question", "answer"])
    df["question"] = df["question"].str.strip()
    df["answer"] = df["answer"].str.strip()
    df = df[(df['answer'].str.len() < 8000) & (df['question'].str.len() < 2000)]

    return df

def df_to_documents(df, max_chars=8000):
    """Convert Q&A dataframe to LangChain Document objects, trimming content."""
    docs = []
    for _, row in df.iterrows():
        content = f"Question: {row['question']}\nAnswer: {row['answer']}"
        if len(content) > max_chars:
            content = content[:max_chars]  # Truncate long content
        docs.append(Document(
            page_content=content,
            metadata={key: row[key] for key in df.columns if key not in ('question', 'answer')}
        ))
    return docs


if __name__ == "__main__":
    df = load_medquad()
    docs = df_to_documents(df)
    print(f"Loaded {len(docs)} cleaned Q&A pairs for retrieval.")
