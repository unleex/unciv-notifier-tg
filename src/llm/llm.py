from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

class LLM():

    def __init__(
            self, 
            credentials: str, 
            system_prompt: str | None = None,
            temperature: float = 0.7,
            max_tokens: int = 100,
            verify_ssl_certs: bool = False
            ):
        self.model = GigaChat(
            credentials=credentials,
            verify_ssl_certs=verify_ssl_certs
        )
        self.payload = Chat(
            messages=[
                Messages(
                role=MessagesRole.SYSTEM,
                content=system_prompt
            ) 
            ] if system_prompt is not None else [],
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def prompt(self, text: str, remember: bool = True): 
        self.payload.messages.append(
            Messages(role=MessagesRole.USER, content=text)
            )
        try:
            response = self.model.chat(self.payload)
        except Exception as e:
            print(f"An exception occured from Gigachat API!: {e}")
        message = response.choices[0].message
        if remember:
            self.payload.messages.append(message)
        else:
            # remove prompt
            self.payload.messages.pop()
        return message.content