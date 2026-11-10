from langchain.chat_models import init_chat_model
from langchain import hub
from utils.db_manager import save_qa

prompt = hub.pull("rlm/rag-prompt")

def is_answer_sufficient(question, answer):
    if len(answer) < 30:
        return False
    if answer.count(".") < 3:
        return False
    q_words = set(question.lower().split())
    if not q_words.intersection(set(answer.lower().split())):
        return False
    return True


class TemperatureRetryAgent:
    def __init__(self, model_name="gemini-2.5-flash-lite", provider="google_genai",
                 min_temp=0.3, max_temp=0.9, step=0.2, max_attempts=4):
        self.model_name = model_name
        self.provider = provider
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.step = step
        self.max_attempts = max_attempts

    def run(self, question: str, context):
        docs_content = "\n\n".join(doc.page_content for doc in context)
        temperature = self.min_temp
        attempt = 0
        answer = ""
        user_id = "default_user"  # İstersen burada user_id’yi dışarıdan alabilirsin

        while attempt < self.max_attempts and temperature <= self.max_temp:
            llm = init_chat_model(self.model_name, model_provider=self.provider, temperature=temperature)
            messages = prompt.invoke({"question": question, "context": docs_content})
            response = llm.invoke(messages)
            answer = response.content.strip()

            if is_answer_sufficient(question, answer):
                break

            temperature += self.step
            attempt += 1

        save_qa(question, answer, user_id)
        return answer
