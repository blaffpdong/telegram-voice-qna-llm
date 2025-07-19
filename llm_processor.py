# llm_processor.py
# https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/blob/main/mistral-7b-instruct-v0.2.Q5_K_M.gguf

from llama_cpp import Llama


class LLMProcessor:
    """
    Class for handling requests to the LLM model with preset parameters.

    Attributes:
        llm (Llama): Initialized instance of the Llama model
        system_prompt (str): Default system prompt
    """

    def __init__(
        self,
        repo_id: str = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        filename: str = "mistral-7b-instruct-v0.2.Q5_K_M.gguf",
        system_prompt: str = None,
        verbose: bool = False,
    ):
        """
        Initialize the model with default or user-defined parameters.

        Args:
            repo_id: Model repository ID
            filename: GGUF model file name
            system_prompt: User-defined system prompt
            verbose: Verbose mode
        """
        self.llm = Llama.from_pretrained(
            repo_id=repo_id,
            filename=filename,
            verbose=verbose,
            n_ctx=1024,
            chat_format="llama-2"
        )

        self.system_prompt = (
            system_prompt
            or """
        You are a candidate's stand-in for an interview.
        Respond briefly, precisely, and professionally.
        The interview consists of 80% hard skills and 20% soft skills.
        If a question requires a personal response, answer using the pronoun "I."
        Be as concise as possible: 1-2 sentences per question, just the essence.
        If a question is incorrect or unclear, reply with "Incorrect question."
        Do not add explanations, apologies, or offers of assistance.
        Identify the question's language accurately and respond in the same language.
        """
        )

    def generate_response(
        self, prompt: str, language: str = None, max_tokens: int = 256
    ) -> str:
        """
        Generating a response based on the prompt using the Mistral template.

        Args:
            prompt: User query text
            max_tokens: Maximum number of tokens in the response

        Returns:
            str: Generated response text
        """
        # Forming the system prompt
        system_content = self.system_prompt
        if language:
            system_content = f"Please respond in {language}\n{system_content}"

        # Creating the message structure
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ]

        # Calling the chat API
        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            stop=["</s>", "<</SYS>>", "/[INST]"],
            temperature=0.0,
            repeat_penalty=1.0,
        )

        return response["choices"][0]["message"]["content"]


# Example of use if run as a script
# $ python llm_processor.py
if __name__ == "__main__":
    processor = LLMProcessor()
    response = processor.generate_response("How many stars are in the sky right now?")
    print(response)
