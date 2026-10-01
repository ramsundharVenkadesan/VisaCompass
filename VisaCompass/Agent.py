import json

from langchain_core.messages import HumanMessage
from ExecutableTools.ECFR import *
from ExecutableTools.GuidanceSources import *
from ExecutableTools.GOV_INFO import *
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from Prompt import react_system_instructions
from StructuredModels import ImmigrationResponse
from langsmith import traceable

load_dotenv()

llm = init_chat_model(model_provider="google-genai",
                      model="gemini-3.5-flash",
                      temperature=0)

tools = [
    search_gov_info, get_gov_info_granules, get_gov_info_package_summary,
    search_ecfr_immigration, get_ecfr_section_text, get_ecfr_title_text,
    search_uscis_data, search_dos_stamping_data, search_dhs_data,
    get_immigration_lawyer_advice, crawl_dhs_data
]

react_agent = create_agent(
    model=llm,
    system_prompt=react_system_instructions,
    response_format=ImmigrationResponse,
    tools=tools
)

@traceable(name="Immigration Agent Execution")
async def stream_query(question:str):
    react_steps, tools_used = [], []
    final_structured_response = None
    inputs = {"messages": [HumanMessage(content=question)]}
    
    try:
        async for event in react_agent.astream_events(inputs, version="v2"):
            kind = event.get("event")
            name = event.get("name", "")

            if kind == "on_tool_start":
                # Only track actual tools, skip the output schema tool
                if name not in ["ImmigrationResponse"]:
                    if name not in tools_used:
                        tools_used.append(name)
                    input_data = event.get("data", {}).get("input", "")
                    step_info = {
                        "step": "Action", "tool": name,
                        "input": str(input_data)[:150]
                    }
                    react_steps.append(step_info)
                    yield f"data: {json.dumps({'type': 'react_step', 'step': step_info})}\n\n"

            elif kind == "on_tool_end":
                if name not in ["ImmigrationResponse"]:
                    output = event.get("data", {}).get("output", "")
                    step_info = {
                        "step": "Observation", "tool": name,
                        "output": str(output)[:200] + "..."
                    }
                    react_steps.append(step_info)
                    yield f"data: {json.dumps({'type': 'react_step', 'step': step_info})}\n\n"
            
            elif kind == "on_chain_end" and name == "LangGraph":
                # The top level agent graph finished, we can extract the final output
                output_data = event.get("data", {}).get("output", {})
                
                # Depending on langchain internals, it's either in structured_response or we parse the AIMessage
                if "structured_response" in output_data:
                    final_structured_response = output_data["structured_response"]
                else:
                    # Fallback to the last AIMessage tool calls:
                    messages = output_data.get("messages", [])
                    if messages and hasattr(messages[-1], "tool_calls"):
                        for call in messages[-1].tool_calls:
                            if call["name"] == "ImmigrationResponse":
                                final_structured_response = call["args"]
                                break

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    # Convert Pydantic to dict if needed
    if hasattr(final_structured_response, "dict"):
        final_structured_response = final_structured_response.dict()
    elif hasattr(final_structured_response, "model_dump"):
        final_structured_response = final_structured_response.model_dump()

    final_payload = {
        "type": "done",
        "answer": final_structured_response,
        "tools_used": list(set(tools_used)),
        "react_steps": react_steps
    }

    yield f"data: {json.dumps(final_payload)}\n\n"
    yield "data: [DONE]\n\n"
