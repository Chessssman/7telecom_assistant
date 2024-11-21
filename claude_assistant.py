import anthropic

class ClaudeAssistant:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_answer(self, question, context):
        try:
            prompt = f"""You are a helpful AI assistant. 
            Context from available documents:
            {context}

            Question: {question}

            Please provide a comprehensive and precise answer based on the context. 
            If the answer cannot be directly found in the context, please indicate so clearly."""

            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"