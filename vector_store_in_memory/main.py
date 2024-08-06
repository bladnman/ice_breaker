import datetime
import os

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

VECTOR_STORE_FILE_PATH = "faiss_index_react"


def get_documents():
  return PyPDFLoader("react_reasoning_and_acting_in_llm.pdf").load()


def get_chunks(documents):
  return CharacterTextSplitter(
    chunk_size=1000, chunk_overlap=3, separator="\n"
  ).split_documents(documents)


def get_vectorstore(chunks):
  embeddings = OpenAIEmbeddings()

  vectorstore = FAISS.from_documents(
    chunks,
    embeddings,
  )

  save_vector_store(vectorstore, VECTOR_STORE_FILE_PATH)

  return vectorstore


def save_vector_store(vectorstore, file_path):
  vectorstore.save_local(file_path)


def get_saved_vector_store(file_path):
  if not os.path.exists(file_path):
    return None

  return FAISS.load_local(file_path, OpenAIEmbeddings())


def get_qa_chain_for_vectorstore(vectorstore):
  return RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
  )


def create_qa_chain():
  vectorstore = get_saved_vector_store(VECTOR_STORE_FILE_PATH)

  if vectorstore is None:
    print("looks like we have to create the vectorstore")
    chunks = get_chunks(get_documents())
    vectorstore = get_vectorstore(chunks)

  return get_qa_chain_for_vectorstore(vectorstore)


def main():
  qa_chain = create_qa_chain()

  ask_qa_chain(
    qa_chain,
    "Please summarize the paper in a few sentences."
  )
  ask_qa_chain(
    qa_chain,
    "Can you tell me a bit more detail around the ReAct algorithm?"
  )


def ask_qa_chain(qa, query):
  start = datetime.datetime.now()
  print("-" * 30)
  print(f"Posing Question:")
  print(f"{query} ...")

  answer = qa({"query": query})

  print()
  print(f"Answer:")
  print(f"{answer['result']}")

  print_time_delta(datetime.datetime.now() - start)


def print_time_delta(delta):
  seconds = delta.total_seconds()

  minutes = seconds // 60
  seconds %= 60

  hours = minutes // 60
  minutes %= 60

  days = hours // 24
  hours %= 24

  time_parts = []
  if days:
    time_parts.append(f"{int(days)}:")
  if hours:
    time_parts.append(f"{int(hours)}:")
  if minutes:
    time_parts.append(f"{int(minutes)}:")
  if seconds:
    time_parts.append(f"{int(seconds)}s")

  if time_parts:
    time_string = ''.join(time_parts)
    print(f"Think time: {time_string}")
  else:
    print("No time elapsed.")


if __name__ == "__main__":
  main()
