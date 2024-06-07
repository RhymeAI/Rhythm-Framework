"""A module containing all QDrant API integrations."""

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.qdrant import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from qdrant_client.http import models
from qdrant_client import QdrantClient

class Vector_DB():
    """An interface with qdrant vector databases."""

    def __init__(self, db_name : str, db_url : str | None = None, db_api_key : str | None = None, embeddings_api_key : str | None = None) -> None:
        """An interface with qdrant vector databases.

        Arguments:

            `db_name`: The name of the database.
            `db_url`: The qdrant database url, leave as `None` to use the enviorment variable `QDRANT_DATABASE_URL`.
            `db_api_key`: The qdrant API key, leave as `None` to use the enviorment variable `QDRANT_API_KEY`.
            `embeddings_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.
                
        Examples:

        .. code-block:: python
            from rhythm.integrations import Vector_DB
        
            vector_db = Vector_DB(db_name=\"example\")"""

        db_url = db_url or os.environ.get("QDARANT_DATABASE_URL")
        db_api_key = db_api_key or os.environ.get("QDRANT_API_KEY")
        embeddings_api_key = embeddings_api_key or os.environ.get("OPENAI_API_KEY")

        self.__db_name = db_name
        client = QdrantClient(url=db_url, api_key=db_api_key)
        embeddings = OpenAIEmbeddings(api_key=embeddings_api_key)
        self.__vector_store = Qdrant(client=client, collection_name=db_name, embeddings=embeddings)

    def add_to_db(self, text: str) -> None:
        """Add an entry to the database.

        Arguments:

            `text`: The text to add to the database."""

        textSplitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = textSplitter.split_text(text)
        self.__vector_store.add_texts(texts = docs)

    def get_from_db(self, query: str, max_amount : int, accuracy : float) -> list[str]:
        """Query the database.

        Arguments:

            `query`: The text query for the database.
            `max_amount`: The maximum amount of entries returned, if they meet the accuracy.
            `accuracy`: The minimum amount an entry needs to match the query, needs to be between `0` and `1` inclusive.

        Returns: 
        
            A list of matching entries in the database."""

        result = self.__vector_store.similarity_search_with_score(query=query, k=max_amount)
        results = []
        for doc in result:
            if(doc[1] >= accuracy):
                results.append(doc[0].page_content)
        return results

    def reset_db(self) -> None:
        """Reset the database."""

        self.__vector_store.client.delete_collection(self.__db_name)
        self.__vector_store.client.create_collection(collection_name=self.__db_name, vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))
