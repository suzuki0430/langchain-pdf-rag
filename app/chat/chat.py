import random
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import (
    set_conversation_components,
    get_conversation_components
)
from app.chat.score import random_component_by_score


def select_component(
    component_type, component_map, chat_args
):
    components = get_conversation_components(
        chat_args.conversation_id
    )
    previous_component = components[component_type]

    if previous_component:
        # 二回目以降のメッセージ。一回目と同じComponentを使う。
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        # 一回目のメッセージ。ランダムでComponentを選ぶ。
        # random_name = random.choice(list(component_map.keys()))
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    print(chat_args)

    retriever_name, retriever = select_component(
        "retriever",
        retriever_map,
        chat_args
    )
    llm_name, llm = select_component(
        "llm",
        llm_map,
        chat_args
    )
    memory_name, memory = select_component(
        "memory",
        memory_map,
        chat_args
    )
    print(
        f"Running chain with: memory: {memory_name}, llm: {llm_name}, retriever: {retriever_name}"
    )
    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name
    )

    condense_question_llm = ChatOpenAI(streaming=False)

    # 脈絡のない質問をしても対応できるようにする
    # 二回目以降の質問とメモリ上の会話履歴からLLMで新しく質問をつくる
    # 新しく作成した質問とRetrieverの情報からLLMで回答をもらう
    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever
    )
