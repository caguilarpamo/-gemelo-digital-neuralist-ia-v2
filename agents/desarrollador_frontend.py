# agents/desarrollador_frontend.py
# NOTE: Written for langchain>=1.2 / langgraph>=1.1 where AgentExecutor and
# create_react_agent have been replaced by create_agent (returns a CompiledStateGraph).
# The public interface (DesarrolladorFrontEndAgent.run) is unchanged.
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

from llm.provider import get_llm
from tools.stitch_tools import create_stitch_project, generate_screen, save_and_convert_to_react

_SYSTEM_PROMPT = """ROL: Senior Frontend Developer. Construye la UI usando Google Stitch.
INPUT: Plan frontend del Líder Técnico.
PASOS (en orden):
1. create_stitch_project UNA vez (título derivado del plan).
2. Identifica las pantallas del plan (mínimo 1).
3. generate_screen por cada pantalla (usa su descripción como prompt).
4. save_and_convert_to_react por cada pantalla generada.
5. Resume: lista los paths de los .jsx generados."""


class DesarrolladorFrontEndAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = [create_stitch_project, generate_screen, save_and_convert_to_react]
        self._agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=_SYSTEM_PROMPT,
            debug=True,
        )

    def run(self, plan_tecnico: str) -> str:
        inputs = {"messages": [HumanMessage(content=plan_tecnico)]}
        result = self._agent.invoke(inputs, config={"recursion_limit": 30})
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content:
                return msg.content
        return "Frontend generation completed."
