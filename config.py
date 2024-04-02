import os,tiktoken, openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.evaluation import load_evaluator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())  # Read local .env file
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Safely load the OpenAI API key

# Configuration for language models and embeddings
gpt_model = "gpt-3.5-turbo"
embedding = OpenAIEmbeddings()  # Initialize OpenAI embedding, e.g., "text-embedding-ada-002"
evaluator_embedding = load_evaluator("embedding_distance")  # Default to Cosine Similarity for embedding

# Accuracy criteria for evaluating LLM responses
accuracy_criteria = {
    "accuracy": """
Score 1: Completely unrelated to the reference.
Score 3: Minor relevance but does not align with the reference.
Score 5: Moderate relevance but contains inaccuracies.
Score 7: Aligns with reference but minor errors or omissions.
Score 10: Completely accurate and perfectly aligns with the reference."""
}

# Initialize evaluators for accuracy and labeled scoring
evaluator_accuracy = load_evaluator(
    "labeled_score_string",
    criteria=accuracy_criteria,
    llm=ChatOpenAI(model="gpt-4"),  # Using GPT-4 for evaluation
)

# Initialize the Language Model (LLM) for ChatGPT
llm = ChatOpenAI(model_name=gpt_model, temperature=0)

# OpenAI Pricing details for cost calculations
embedding_token_cost = 1e-08
gpt_input_token_cost = 5e-08
gpt_output_token_cost = 1.5e-06


# Function to count the tokens in a given text, considering the model used
def num_tokens(text: str, model: str = gpt_model) -> int:
    """Calculates and returns the number of tokens in the provided text string.

    Args:
        text (str): The text to tokenize.
        model (str, optional): The model used for tokenization. Defaults to gpt_model.

    Returns:
        int: The total number of tokens.
    """
    encoding = tiktoken.encoding_for_model(model)  # Get the encoding for the specified model
    return len(encoding.encode(text))

