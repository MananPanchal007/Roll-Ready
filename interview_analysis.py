from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List
import os

SYSTEM_PROMPT = """You are an expert interview analyst. Analyze the interview conversation and provide a concise summary (200 words) focusing on:

1. Communication skills
2. Technical knowledge
3. Problem-solving approach
4. Key strengths
5. Areas for improvement

Keep the analysis clear and actionable."""

class InterviewAnalyzer:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Please analyze this interview conversation:\n\n{conversation}")
        ])

    def analyze_conversation(self, conversation: List[Dict]) -> str:
        """Analyze the interview conversation and generate a summary."""
        try:
            formatted_conversation = self._format_conversation(conversation)
            response = self.llm.invoke(self.prompt.format(conversation=formatted_conversation))
            return response.content
        except Exception as e:
            print(f"Error generating analysis: {str(e)}")
            return "Error generating analysis. Please try again."

    def _format_conversation(self, conversation: List[Dict]) -> str:
        """Format the conversation for analysis."""
        return "\n".join([
            f"{'Interviewer' if msg['role'] == 'ai' else 'Candidate'}: {msg['content']}"
            for msg in conversation
        ])

    def update_system_prompt(self, new_prompt: str):
        """Update the system prompt for analysis."""
        global SYSTEM_PROMPT
        SYSTEM_PROMPT = new_prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Please analyze this interview conversation:\n\n{conversation}")
        ]) 