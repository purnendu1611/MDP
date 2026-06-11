from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from utils.prompts import MEDICAL_QA_PROMPT, SUMMARY_PROMPT


class MedicalRAGPipeline:

    def __init__(self, persist_dir: str = ".chroma_db"):
        self.persist_dir = persist_dir

        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.embeddings = OpenAIEmbeddings()

        # chunk size 1000 with 200 overlap worked best in testing —
        # smaller chunks caused lab values to get split mid-row
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "],
        )

        self.vectorstore = Chroma(
            collection_name="medical_docs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir,
        )

    def add_document(self, file_obj) -> int:
        tmp_path = Path(f"/tmp/{file_obj.name}")
        tmp_path.write_bytes(file_obj.read())

        loader = PyPDFLoader(str(tmp_path))
        pages = loader.load()

        for page in pages:
            page.metadata["source_file"] = file_obj.name

        chunks = self.splitter.split_documents(pages)
        self.vectorstore.add_documents(chunks)
        tmp_path.unlink(missing_ok=True)
        return len(chunks)

    def add_text(self, text: str, source: str = "manual_input") -> int:
        doc = Document(page_content=text, metadata={"source_file": source})
        chunks = self.splitter.split_documents([doc])
        self.vectorstore.add_documents(chunks)
        return len(chunks)

    def query(self, question: str, k: int = 4) -> dict[str, Any]:
        # MMR search helps avoid getting 4 chunks from the same page
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": 10},
        )
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": MEDICAL_QA_PROMPT},
        )
        result = chain.invoke({"query": question})

        sources = [
            {
                "content": doc.page_content,
                "page": doc.metadata.get("page", "?"),
                "file": doc.metadata.get("source_file", "unknown"),
            }
            for doc in result.get("source_documents", [])
        ]
        return {"answer": result["result"], "sources": sources}

    def summarize(self) -> str:
        # TODO: this grabs top-k chunks by similarity which misses some sections
        # a better approach would be map-reduce over all chunks
        docs = self.vectorstore.similarity_search("main findings diagnosis treatment", k=8)
        combined = "\n\n".join(d.page_content for d in docs)
        prompt = SUMMARY_PROMPT.format(report_text=combined)
        response = self.llm.invoke(prompt)
        return response.content

    def clear(self) -> None:
        self.vectorstore.delete_collection()
        self.vectorstore = Chroma(
            collection_name="medical_docs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir,
        )
