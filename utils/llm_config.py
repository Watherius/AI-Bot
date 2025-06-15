from decouple import config
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.create_history import get_history

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=config('OPENAI_API_KEY'),
    temperature=0.3
)

template="""
        Ты — профессиональный менеджер по продажам автомобилей. 
        Всю информацию о текущем клиенте бери из JSON ниже и автоматически извлекай любые поля:
        {crm_json}

        Дальше:
        – Приветствуй один раз.
        – Сразу предложи две–три модели в его бюджете.
        – Если целевая модель стоит дороже, предложи подержанные или альтернативы.
        – В конце всегда сделай лёгкий upsell.
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{user_input}")
])

chain_without_history = prompt | model | StrOutputParser()

chain = RunnableWithMessageHistory(
    runnable=chain_without_history,
    get_session_history=get_history,
    input_messages_key="user_input",
    history_messages_key="history",
)