import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain import VectorDBQA, OpenAI

import pinecone

pinecone.init(
  api_key="ab3ed2ee-070b-4277-b919-00586ee68a5a",
  environment="us-west4-gcp-free"
)


def get_qa_chain_for_documents(documents):
  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
  chunks = text_splitter.split_documents(documents)

  embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

  vectorstore = Pinecone.from_documents(
    chunks,
    embeddings,
    index_name="medium-blog-embeddings-index"
  )

  qa_chain = VectorDBQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    vectorstore=vectorstore
  )
  return qa_chain


def get_qa_chain_for_vectorstore(vectorstore):
  return VectorDBQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    vectorstore=vectorstore
  )


def main():
  loader = TextLoader("mediumblogs/mediumblog1.txt")
  documents = loader.load()
  qa_chain = get_qa_chain_for_documents(documents)

  ask_qa_chain(
    qa_chain,
    "What is a vector database? Give me a short answer for a beginner."
  )
  ask_qa_chain(
    qa_chain,
    "What values would be found in a vector database? Can you give me an example?"
  )


def ask_qa_chain(qa, query):
  answer = qa({"query": query})

  print("-" * 30)
  print(f"Question:")
  print(f"{answer['query']}")
  print()
  print(f"Answer:")
  print(f"{answer['result']}")


if __name__ == "__main__":
  main()
