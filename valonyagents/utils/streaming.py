import asyncio
from typing import AsyncGenerator, Callable
import streamlit as st
from queue import Queue
from threading import Thread

class StreamHandler:
    def __init__(self):
        self.queue = Queue()
        self.stop_signal = False

    async def stream_callback(self, token: str):
        """Callback function for streaming tokens"""
        if not self.stop_signal:
            self.queue.put(token)
            await asyncio.sleep(0)  # Yield control

    def reset(self):
        """Reset the stream handler"""
        self.stop_signal = False
        while not self.queue.empty():
            self.queue.get()

    def stop(self):
        """Stop the stream"""
        self.stop_signal = True

class StreamingManager:
    @staticmethod
    async def process_stream(handler: StreamHandler, 
                           placeholder: st.empty,
                           processor: Callable[[str], AsyncGenerator[str, None]]):
        """Process streaming content with a given processor"""
        full_response = ""
        
        async for token in processor(""):
            if handler.stop_signal:
                break
                
            await handler.stream_callback(token)
            full_response += token
            placeholder.markdown(full_response + "▌")
        
        placeholder.markdown(full_response)
        return full_response

    @staticmethod
    def run_async_stream(coro):
        """Run async stream in a separate thread"""
        loop = asyncio.new_event_loop()
        
        def run_loop():
            asyncio.set_event_loop(loop)
            loop.run_until_complete(coro)
            
        thread = Thread(target=run_loop)
        thread.start()
        return thread