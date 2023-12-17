from langchain.chains import ConversationalRetrievalChain
from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory

def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    print(chat_args)
    
    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)
    memory = build_memory(chat_args)
    
    # 脈絡のない質問をしても対応できるようにする
    # 二回目以降の質問とメモリ上の会話履歴からLLMで新しく質問をつくる
    # 新しく作成した質問とRetrieverの情報からLLMで回答をもらう
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever
    )