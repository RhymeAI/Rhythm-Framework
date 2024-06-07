# Vector_DB (Class)

An interface with qdrant vector databases.

## Initialization

#### Arguments

> `db_name`: The name of the database.  
> `db_url`: The qdrant database url, leave as `None` to use the enviorment variable `QDRANT_DATABASE_URL`.  
> `db_api_key`: The qdrant API key, leave as `None` to use the enviorment variable `QDRANT_API_KEY`.  
> `embeddings_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.

#### Examples:

```python
from rhythm.integrations import Vector_DB

vector_db = Vector_DB(db_name="example")
```

## Methods

### add_to_db

Add an entry to the database.

#### Arguments

> `text`: The text to add to the database.

#### Examples

```python
vector_db.add_to_db(text="Example Text")
```

### get_from_db

Query the database.

#### Arguments

> `query`: The text query for the database.  
> `max_amount`: The maximum amount of entries returned, if they meet the accuracy.  
> `accuracy`: The minimum amount an entry needs to match the query, needs to be between `0` and `1` inclusive.

#### Returns

A list of matching entries in the database.

#### Examples

```python
vector_db.get_from_db(query="Example", max_amount=5, accuracy=0.75)
```

### reset_db

Reset the database.

#### Examples

```python
vector_db.reset_db()
```
