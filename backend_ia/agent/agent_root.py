from google.adk.agents import LlmAgent
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

#agente root do sistema
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="root_agent",
    description="Agente raiz do sistema",
    instruction="""Você é um agente que auxilia um usuário a fazer anotações, voce deve ler oque o usuario passar interpretar ou 
    fazer oque ele pedir para auxiliar nas anotações dele.""",
)