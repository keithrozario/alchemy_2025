from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.tools import ToolContext
from google.genai import types
import uuid
import asyncio
import os

from tools import doc_tools

APP_NAME = "test_app"
USER_ID = "test_user_456"
SESSION_ID = uuid.uuid4().hex
MODEL_NAME = "gemini-2.0-flash"

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = "TRUE"
os.environ['GOOGLE_CLOUD_PROJECT'] = "default-krozario"
os.environ['GOOGLE_CLOUD_LOCATION'] = "us-central1"
os.environ["AGENT_ENGINE_ID"] = "1263761072779689984"


def get_user_upload(tool_context: ToolContext) -> dict:

    with open("./doc_agent/user_uploads/screenshot.png", "rb") as user_upload:
         data = user_upload.read()

    tool_context.save_artifact(
        filename="screenshot.png", 
        artifact=types.Part(
            inline_data=types.Blob(
                mime_type = "image/png",
                data = data
        ))
    )

    return {"status": "OK"}


document_agent = LlmAgent(
    model=MODEL_NAME,
    name="document_agent",
    description="Retrieves the capital city using a specific tool.",
    instruction="""
    You will be provided with a document. 
    Your task is to extract the first name, last name, and address from the document.
    Here is the document:
    """,
    output_schema=doc_tools.DocumentData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

async def call_agent_and_print(
    runner_instance: Runner,
    user_id: str,
    session_id: str,
    user_content: types.Content
):
    """Sends a query to the specified agent/runner and prints results."""

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(user_id=user_id, session_id=session_id, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    return final_response_content


if __name__ == "__main__":
    session_service = InMemorySessionService()
    session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    artifact_service = InMemoryArtifactService()

    document_runner = Runner(
        agent=document_agent,
        app_name=APP_NAME,
        session_service=session_service,
        artifact_service=artifact_service
    ) 

    with open("./doc_agent/user_uploads/screenshot.png", "rb") as user_upload:
        data = user_upload.read()
    query='What is the name in the document?'
    
    user_content = types.Content(role='user', parts=[
        types.Part(text=query),
        types.Part(inline_data=types.Blob(
            mime_type = "image/png",
            data = data
        ))])


    response = asyncio.run(call_agent_and_print(
        runner_instance=document_runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
        user_content=user_content)
    )

    print(response)
    
    with open("./doc_agent/user_uploads/property_deed.pdf", "rb") as user_upload:
        data = user_upload.read()
    query='What is the name in the document?'
    
    user_content = types.Content(role='user', parts=[
        types.Part(text=query),
        types.Part(inline_data=types.Blob(
            mime_type = "application/pdf",
            data = data
        ))])


    response = asyncio.run(call_agent_and_print(
        runner_instance=document_runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
        user_content=user_content)
    )
    
    print(response)