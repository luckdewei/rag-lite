import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collections = client.list_collections()
for collection in collections:
    results = collection.get(include=["documents", "metadatas", "embeddings"])
    ids = results["ids"]
    documents = results["documents"]
    metadatas = results["metadatas"]
    embeddings = results["embeddings"]
for i, (id, doc, meta, embedding) in enumerate(
    zip(ids, documents, metadatas, embeddings)
):
    print(f"第{i}条: {id} {doc} {meta} {embedding}")
