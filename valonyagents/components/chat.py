import streamlit as st
from typing import List, Dict
from utils.streaming import StreamHandler, StreamingManager

class ChatInterface:
    def __init__(self):
        self.stream_handler = StreamHandler()
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display_message(self, role: str, content: str, placeholder=None):
        """Display a single message in the chat interface"""
        if placeholder:
            with placeholder.container():
                st.markdown(f"**{role}**: {content}")
        else:
            st.markdown(f"**{role}**: {content}")

    def display_chat_history(self):
        """Display the entire chat history"""
        for message in st.session_state.messages:
            self.display_message(message["role"], message["content"])

    def add_message(self, role: str, content: str):
        """Add a message to the chat history"""
        st.session_state.messages.append({"role": role, "content": content})

    async def process_user_input(self, 
                               user_input: str,
                               response_placeholder: st.empty,
                               crew_manager) -> str:
        """Process user input and generate response"""
        self.add_message("user", user_input)
        
        # Create inputs dictionary for the crew
        inputs = {
            "query": user_input,
            "chat_history": st.session_state.messages
        }
        
        # Process with CrewAI
        response = await StreamingManager.process_stream(
            self.stream_handler,
            response_placeholder,
            lambda _: crew_manager.process_async(inputs)
        )
        
        self.add_message("assistant", response)
        return response

    def render(self, crew_manager):
        """Render the chat interface"""
        st.title("Support Data Analysis Chat")
        
        # Display chat history
        self.display_chat_history()
        
        # Chat input
        user_input = st.chat_input("What would you like to analyze?")
        if user_input:
            # Create placeholder for streaming response
            response_placeholder = st.empty()
            
            # Process user input
            StreamingManager.run_async_stream(
                self.process_user_input(
                    user_input,
                    response_placeholder,
                    crew_manager
                )
            )