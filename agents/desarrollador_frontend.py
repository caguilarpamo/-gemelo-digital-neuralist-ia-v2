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

LÍMITES ESTRICTOS (no excedas):
- MÁXIMO 3 pantallas. Si el plan menciona más, elige las 3 más importantes.
- UNA sola llamada a generate_screen por pantalla.
- UNA sola llamada a save_and_convert_to_react por pantalla.

PASOS:
1. create_stitch_project UNA vez (título corto del plan).
2. Selecciona las 3 pantallas más críticas.
3. generate_screen por cada una (descripción breve, no el plan completo).
4. save_and_convert_to_react por cada una.
5. Resume con los paths de los .jsx generados."""


class DesarrolladorFrontEndAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = [create_stitch_project, generate_screen, save_and_convert_to_react]
        self._agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=_SYSTEM_PROMPT,
            debug=False,
        )

    def run(self, plan_tecnico: str) -> str:
        inputs = {"messages": [HumanMessage(content=plan_tecnico)]}
        result = self._agent.invoke(inputs, config={"recursion_limit": 30})
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content:
                return msg.content
        return "Frontend generation completed."
