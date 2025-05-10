from langchain.prompts import ChatMessagePromptTemplate
from langchain.llms import ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval_qa.base import RetrievalQA


def create_chain(retriever):
    prompt=ChatMessagePromptTemplate.from_template("""
                                                   Your a review anyalists of a food company,stay focused on context and anser in as humanly psobblem with correct information.
                                                   Think step by step and give the best output.
                                                   <context>
                                                   {context}
                                                   <context>
                                                   Question:{input}
                                                   """)
    
    model=ollama("llama2")
    qa_chain=RetrievalQA.from_chain_type(llm=model,retriever=retriever,chain_type="stuff",prompt=prompt)





