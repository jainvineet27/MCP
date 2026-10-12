import os
import shutil
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from ingestion_postgres import insert_into_pgdb, create_embeddings, create_engine


def load_files(source_folder="source_files", target_folder="processed_files"):

    print("loading files >>>>>>>>>>>>>>>>> ")

    parent_cwd = os.path.dirname(__file__)
    source_folder = os.path.join(parent_cwd, source_folder)
    target_folder = os.path.join(parent_cwd, target_folder)

    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(target_folder, exist_ok=True)
    if file in os.listdir(source_folder):
        for file in os.listdir(source_folder):
            

            print(f"processing file >>>>>> ", file)
            file_path = os.path.join(source_folder, file)
            try:
                reader = PDFPlumberLoader(file_path)
                documents = reader.load()

                content_list = []
                for doc in documents:
                    content_list.append(doc.page_content+"\n")
                    

                destination_path = os.path.join(target_folder, file)

                shutil.move(file_path, destination_path)
                return content_list

            except Exception as e:
                print(f"Error occured for {file}")


def create_chunks(file_contents):
    chunks_list = []
    ids = []
    metadatas = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=150, separators=["\n\n", "\n", " ", "."])
    chunks = splitter.split_documents(file_contents)
    
    for chunk in chunks:
        chunks_list.append(chunk.page_content)
        ids.append(chunk.id + str(uuid.uuid4()))
        metadatas.append(chunk.metadata)

    return chunks_list, metadatas, ids


if __name__=="__main__":
        
    file_contents = load_files()
    chunks, metadatas, ids = create_chunks(file_contents)
    embeddings = create_embeddings(chunks)
    insert_into_pgdb(contents=chunks, embeddings=embeddings)
    
    

    

