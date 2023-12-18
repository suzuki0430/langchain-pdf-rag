from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()

class StreamingHandler(BaseCallbackHandler):
  def __init__(self, queue):
    self.queue = queue
  
  def on_llm_new_token(self, token, **kwargs):
    self.queue.put(token)
    
  def on_llm_end(self, response, **kwargs):
    self.queue.put(None)
    
  def on_llm_error(self, error, **kwargs):
    self.queue.put(None)

# 分割された出力をqueueにいれる
chat = ChatOpenAI(
  streaming=True,
  # callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
  ("human", "{content}")
])

class StreamableChain:
  def stream(self, input):
    queue = Queue()
    handler = StreamingHandler(queue)
    
    def task():
      self(input, callbacks=[handler]) # 内部的に __call__ メソッドを呼び出し、入力された内容（input）に基づいてLLMを起動し、その結果を生成するプロセスを開始する
    
    Thread(target=task).start() # task 関数を別スレッドで実行する。.start() メソッドを呼び出すことで、スレッドが開始される。この実装により、self(input) の処理がバックグラウンドで実行される間に、メインスレッドは queue からトークンを取得し続けることができる
    
    while True:
      token = queue.get()
      if token is None:
        break
      yield token # yield token は、token を生成し、それを関数の呼び出し元に返すために使用される。この方法により、関数はジェネレータとして振る舞い、ストリーミング処理や遅延評価が可能になる

# 責務を明確に分離し、それぞれのクラスが特化できるようにする
class StreamingChain(StreamableChain ,LLMChain):
  pass

chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content":"tell me a joke"}):
  print(output)

# chain = LLMChain(llm=chat, prompt=prompt)
# for output in chain.stream(input={"content":"tell me a joke"}):
#   print(output)

# messages = prompt.format_messages(content="tell me a joke")
# for message in chat.stream(messages):
#   print(message.content)