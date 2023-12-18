from flask import current_app
from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler

class StreamableChain:
  def stream(self, input):
    queue = Queue()
    handler = StreamingHandler(queue)
    
    # Flaskのアプリケーションコンテキストを別のスレッドで使用する
    def task(app_context):
      app_context.push()
      self(input, callbacks=[handler]) # 内部的に __call__ メソッドを呼び出し、入力された内容（input）に基づいてLLMを起動し、その結果を生成するプロセスを開始する
    
    Thread(target=task, args=[current_app.app_context()]).start() # task 関数を別スレッドで実行する。.start() メソッドを呼び出すことで、スレッドが開始される。この実装により、self(input) の処理がバックグラウンドで実行される間に、メインスレッドは queue からトークンを取得し続けることができる
    
    while True:
      token = queue.get()
      if token is None:
        break
      yield token # yield token は、token を生成し、それを関数の呼び出し元に返すために使用される。この方法により、関数はジェネレータとして振る舞い、ストリーミング処理や遅延評価が可能になる
