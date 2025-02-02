from langgraph.graph import StatefulGraph, START
from typing import Dict, TypedDict, Annotated, Literal
from app.service.extract_transcript import extract_transcript
from app.service.generate_definition import generate_definition
from app.service.glossary import update_glossary

# Definir la estructura del estado con más detalle
class AgentState(TypedDict):
    transcript: str
    definition: str
    glossary_updated: bool
    status: str
    error: str | None

# Funciones para los nodos del grafo con mejor manejo de errores
def process_transcript(state: AgentState) -> Dict[Literal["continue", "error"], AgentState]:
    try:
        state["transcript"] = extract_transcript()
        state["status"] = "transcript_processed"
        return {"continue": state}
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "error"
        return {"error": state}

def create_definition(state: AgentState) -> Dict[Literal["continue", "error"], AgentState]:
    try:
        if not state.get("transcript"):
            raise ValueError("No transcript available")
        
        state["definition"] = generate_definition(state["transcript"])
        state["status"] = "definition_created"
        return {"continue": state}
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "error"
        return {"error": state}

def update_glossary_entry(state: AgentState) -> Dict[Literal["continue", "error"], AgentState]:
    try:
        if not state.get("definition"):
            raise ValueError("No definition available")
        
        update_glossary(state["definition"])
        state["glossary_updated"] = True
        state["status"] = "completed"
        return {"continue": state}
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "error"
        return {"error": state}

def handle_error(state: AgentState) -> AgentState:
    # Función para manejar errores
    print(f"Error occurred: {state['error']}")
    return state

# Crear el grafo
workflow = StatefulGraph(AgentState)

# Añadir nodos al grafo
workflow.add_node("extract_transcript", process_transcript)
workflow.add_node("generate_definition", create_definition)
workflow.add_node("update_glossary", update_glossary_entry)
workflow.add_node("error_handler", handle_error)

# Definir el flujo del grafo con manejo de errores
workflow.add_edge("extract_transcript", "generate_definition", key="continue")
workflow.add_edge("generate_definition", "update_glossary", key="continue")
workflow.add_edge("extract_transcript", "error_handler", key="error")
workflow.add_edge("generate_definition", "error_handler", key="error")
workflow.add_edge("update_glossary", "error_handler", key="error")

# Compilar el grafo
app = workflow.compile()

def run_workflow(initial_state: AgentState = None) -> Dict:
    if initial_state is None:
        initial_state = AgentState(
            transcript="",
            definition="",
            glossary_updated=False,
            status="starting",
            error=None
        )
    return app.invoke(initial_state)


