import os
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import create_engine
from psycopg2 import *

load_dotenv()


PG_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
engine = create_engine(PG_STRING)

client = OpenAI()


def insert_into_pgdb(contents, embeddings):
    data = {}
    for content, embeddings in zip(contents, embeddings):
        data = {"content": content, "embedding": embeddings}

    query = f'''INSERT INTO public.hr_policy_docs 
    (content , embedding) 
    VALUES  (:contents, :embeddings)'''

    with engine.begin() as conn:
        conn.execute(query, data)

    print("Data has been successfully loaded intoo the pgdb")


def retrieve_from_pgdb(query_embedding):

    result = f'''
    select * from public.hr_policy_docs 
    where  {query_embedding} <-> embedding
    '''

    return result.get("documents", "")


def create_embeddings(documents, dimension=300):

    response = client.embeddings.create(model="text-embedding-3-small",
                                        input=documents, dimensions=dimension)
    embeds = []

    for item in response.data:
        embeds.append(item.embedding)

    return embeds
