import os
import openai
from datetime import timezone
import datetime
dt = datetime.datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()
  
print(utc_timestamp)
open_ai_key = os.environ['OPEN_AI_KEY']
openai.api_key = open_ai_key
from agent_prompts import prompts

from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage)
from langchain.memory import ChatMessageHistory

#==========================================
#set up dicts to store each conversation
#==========================================
agents = ['llm1', 'llm2', 'perpetual_agent'] # add more when they're ready

global memory_table
memory_table = {}
global memory_objects
memory_objects = {}
global history_objects
history_objects = {}
global memory_chains
memory_chains = {}
global conversation_objects
conversation_objects = {}
global chat_prompts
chat_prompts = {}
global chats
chats = {}
global inspections
inspections = []

global llm1_chat
llm1_chat = ChatOpenAI(
      openai_api_key=open_ai_key,
      model_name='gpt-4',
      #model_name = 'gpt-3.5-turbo',
      temperature = 0.7,
      max_tokens = 80
  )

global llm2_chat
llm2_chat = ChatOpenAI(
      openai_api_key=open_ai_key,
      model_name='gpt-4',
      #model_name = 'gpt-3.5-turbo',
      temperature = 0.7,
      max_tokens = 80
  )

global perpetual_agent
perpetual_agent_chat = ChatOpenAI(
      openai_api_key=open_ai_key,
      model_name='gpt-4',
      #model_name = 'gpt-3.5-turbo',
      temperature = 0.7,
      max_tokens = 80
  )

chats['llm1'] = llm1_chat
chats['llm2'] = llm2_chat
chats['perpetual_agent'] = perpetual_agent_chat

global chat_summary
chat_summary = ChatOpenAI(
    openai_api_key=open_ai_key,
    model_name='gpt-3.5-turbo',
    temperature = 0.5,
    max_tokens = 100
)

for agent in agents:
  conversation_objects[agent] = {}
  history_objects[agent] = {}
  memory_objects[agent] = ConversationSummaryBufferMemory(llm = chat_summary, return_messages = True, max_token_limit=10000)
  #memory_objects[character] = ConversationBufferMemory()

  system_template=prompts[agent]
  human_template="{input}"
  system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
  human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
  chat_prompts[agent] = ChatPromptTemplate.from_messages([system_message_prompt, MessagesPlaceholder(variable_name="history"), human_message_prompt])
  conversation_objects[agent] = ConversationChain(prompt=chat_prompts[agent], llm=chats[agent], memory = memory_objects[agent], verbose=True)
  history_objects[agent] = ChatMessageHistory()

#==========================================
#define LLMs
#==========================================
def run_llm1(input_text):
  # LLM1 is an AI that believes it is in a conversation with a human
  
  print('=========================')
  print("activating llm_1")
  print('=========================')
  history_objects['llm1'].add_user_message(input_text)
  
  resp = conversation_objects['llm1'].predict_and_parse(input=input_text) 
  history_objects['llm1'].add_ai_message(resp)
  print("LLM1: ", resp, '\n')


def run_llm2(input_text):
  # LLM2 is an AI that believes it is in a conversation with a human
  
  print('=========================')
  print("activating llm_2")
  print('=========================')
  history_objects['llm2'].add_user_message(input_text)
  
  resp = conversation_objects['llm2'].predict_and_parse(input=input_text) 
  history_objects['llm2'].add_ai_message(resp)
  print("LLM2: ", resp, '\n')

#==========================================
#define Perpetual Agent
#==========================================
def run_perpetual_agent():
  print('=========================')
  print("activating agent")
  print('=========================')
  
  agent_prompt = prompts['perpetual_agent']
  p = [{'role':'system', 'content':agent_prompt}]

  for message in history_objects['llm2'].messages[-10:]:
    if message.type == 'human':
      p[0]['content'] += "LLM 1: "+message.content+"\n"
    if message.type == 'ai':
      p[0]['content'] += "LLM 2: "+message.content+"\n"
  #print(p)
  
  analysis_check = openai.ChatCompletion.create(
          model='gpt-4',  
          messages=p,
          temperature = 0.8,
          #top_p = 0.1,
          max_tokens = 256,
        )
  inspection = analysis_check['choices'][0]['message']['content']
  inspections.append(inspection)
  print("INSPECTION: ",inspection,'\n')



#==========================================
#start the perpetual(ish) loop
#==========================================
llm1_start = "Just finished acquisition talks for a sick new digital media startup. Really transforming the potential for hyperconnected virtual experiences. We're probably overpaying, but what the hell, gotta ride the lightning."

llm2_start = "Interesting. Tell me more."

history_objects['llm1'].add_ai_message(llm1_start)
memory_objects['llm1'].chat_memory.add_ai_message(llm1_start)

history_objects['llm2'].add_ai_message(llm2_start)
memory_objects['llm2'].chat_memory.add_ai_message(llm2_start)

inspections.append("[First interaction]")

now = datetime.datetime.now()
date_string = now.strftime("%Y%m%d%H%M%S")
directory = "chats"
os.makedirs(directory, exist_ok=True)

# Create the file name with the generated string
file_name = os.path.join(directory, f"chat-{date_string}.txt")


for i in range(1,21):  # number of iterations 
  with open(file_name, "a") as f:
        output = "====================\n ITERATION " + str(i) + "\n====================\n"
        f.write(output)
        print(output)
        last_llm1 = "LLM 1 (Kendall Roy): " + history_objects['llm1'].messages[-1].content + "\n\n"
        last_llm2 = "LLM 2 (Agreeable AI): " + history_objects['llm2'].messages[-1].content + "\n\n"
        last_inspection = "Perpetual Agent analysis: " + inspections[-1] + "\n"
        f.write(last_llm1)
        f.write(last_llm2)
        f.write(last_inspection)
        

  last_llm1_msg = history_objects['llm1'].messages[-1].content
  run_llm2(last_llm1_msg)
  last_llm2_msg = history_objects['llm2'].messages[-1].content
  run_llm1(last_llm2_msg)
  
  run_perpetual_agent()

