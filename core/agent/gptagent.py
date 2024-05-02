from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os

# Initialize the conversation chain
memory = ConversationBufferMemory(memory_key="history")
llm = OpenAI(temperature=0)  # Use OpenAI from langchain.llms
conversation = ConversationChain(llm=llm, memory=memory)

class OpenAIGPT3Agent():

    @staticmethod
    def get_prompt(query_to_ask, response):

        #Prompt for our agent
        prompt = f"""You are a helpful assistant who can help with some task
                    Task: Give a Question as Question: and Answer as Answer: . Please rephrased Answer in such a way that it matches the  Question asked.
                    Intructions:
                    1) Do not answer anything which is not in the question asked
                    2) Do not answer any other word which is not in question
                    3) Answers should be word to word match if the question is a word to word match
                    4) If you feel like you cannot answer just say "Data Not Available"
                    Take a deep breath and check carefully your answer and verify your answer if it matches with the given question

                    Few Examples:
                    Question: Who is the CEO of the company?
                    Answer: Shruti Gupta
                    Correct Rephrased Answer: Shruti Gupta is the CEO of the company

                    Question: What is the name of the company?
                    Answer: Zania Inc
                    Correct Rephrased Answer: Zania Inc is the name of the company.
                
                    Now having the understanding of the examples and intructions and task please rephrase this Answer: , based on the Question:
                    Question : {query_to_ask}
                    
                    Answer: {response}
        """
        return prompt
    
    @staticmethod
    def getconversation(prompt):
        #RePhrased  answer
        response_new = conversation.predict(input=prompt)
        return response_new
