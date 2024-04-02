import time, config, database
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from typing import List, Tuple



# Define a template for generating prompts for the language model
template = """
You are a helpful chatbot to answer readers' questions./n 
Keep the answer as concise as possible and within 50 words/n
If the question is not related, adopt an empathetic and understanding tone to answer.

{context}
Answer the question based on the context: {question}
Helpful Answer:
"""

# Initialize a PromptTemplate object for structured prompt creation
QA_CHAIN_PROMPT_CAAS = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)


# Initialize the RetrievalQA chain with specified configurations
qa_chain = RetrievalQA.from_chain_type(
    config.llm,  # Predefined language model
    retriever=database.vectordb.as_retriever(),  # Convert vector database to a retriever
    return_source_documents=True,  # Include source documents in the result
    chain_type_kwargs={
        "verbose": True,
        "prompt": QA_CHAIN_PROMPT_CAAS,
        "memory": ConversationBufferMemory(
            memory_key="chat_history",
            input_key="question"
        ),
    }
)

def ask(prompt: str) -> Tuple[str, List[str], str, float, float, str, float, str, int, int, int, int]:
    """
    Process a query using a RetrievalQA chain and evaluate the result.

    Args:
        prompt (str): The user query to process.

    Returns:
        Tuple: A tuple containing the query, source documents, result, scores, runtime, cost estimation,
               and token counts.
    """
    start_time = time.time()  # Start of computing time
    result = qa_chain({"query": prompt})  # Process the query with the QA chain
    end_time = time.time()  # End of computing time
    runtime = round(end_time - start_time, 2)  # Calculate the runtime

    # Cost & Token Counting for query, embedding, and result
    embedding_count = sum(config.num_tokens(doc.page_content) for doc in result['source_documents'])
    query_count, result_count = config.num_tokens(result['query']), config.num_tokens(result['result'])
    cost_estimation = (embedding_count * config.embedding_token_cost +
                       query_count * config.gpt_input_token_cost +
                       result_count * config.gpt_output_token_cost)

    # Evaluate embedding distance score for source documents
    unique_sources = list(set(str(doc) for doc in result['source_documents']))
    rag_score_list = [round(config.evaluator_embedding.evaluate_strings(
                            prediction=result['result'], 
                            reference=doc.page_content)['score'], 2) for doc in result['source_documents']]
    rag_score = sum(rag_score_list) / len(rag_score_list) if rag_score_list else 0

    # Evaluate accuracy based on embeddings
    eval_accuracy = config.evaluator_accuracy.evaluate_strings(
        prediction=result['result'],
        reference=unique_sources,
        input=result['query']
    )
    accuracy_reasoning, accuracy_score = list(eval_accuracy.values())

    # Compile all the relevant information to return
    return (result['query'], unique_sources, result['result'], rag_score, accuracy_score,
            accuracy_reasoning, runtime, f"{cost_estimation:.2e}", query_count, embedding_count,
            result_count, sum([query_count, embedding_count, result_count]))