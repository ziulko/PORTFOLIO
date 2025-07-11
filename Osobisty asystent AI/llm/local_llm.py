from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

def get_local_llm_chain():
    llm = Ollama(model="mistral")
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=(
            "Jesteś osobistym asystentem AI, który prowadzi przyjazną rozmowę po polsku.\n"
            "Jeśli użytkownik się przywita – odpowiedz uprzejmie.\n"
            "Jeśli zapyta 'kim jesteś' – przedstaw się jako lokalny asystent.\n\n"
            "Historia rozmowy:\n{history}\n"
            "Użytkownik: {input}\n"
            "Asystent:"
        )
    )
    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True  # pokazuje logi rozmowy w konsoli
    )

    return chain
