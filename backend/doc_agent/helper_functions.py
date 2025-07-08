import asyncio
from pathlib import Path

from google.adk.runners import Runner
from google.genai import types


async def execute_user_query_async(
    runner_instance: Runner, user_id: str, session_id: str, user_content: types.Content
):
    """Sends a query to the specified agent/runner and prints results."""

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(
        user_id=user_id, session_id=session_id, new_message=user_content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    return final_response_content


def execute_user_query(
    runner_instance: Runner, user_id: str, session_id: str, user_content: types.Content
):
    """Sends a query to the specified agent/runner and prints results."""

    final_response_content = "No final response received."
    for event in runner_instance.run(
        user_id=user_id, session_id=session_id, new_message=user_content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    return final_response_content


def run_query_with_file_data(
    query: str,
    doc_data: bytes,
    doc_mime_type: str,
    runner_instance: Runner,
    user_id: str,
    session_id: str,
) -> str:
    """
    Executes a query to a runner instance together with a document found at doc_path.
    Args:
        query: The Query of the prompt
        doc_path: the Path object of the document
        doc_mime_type: the mime type of the document
        runner_instance: The instance of an ADK runner to execute
        user_id: User ID
        session_id: Session ID

    returns:
        The LLM response as a string
    """

    user_content = types.Content(
        role="user",
        parts=[
            types.Part(text=query),
            types.Part(inline_data=types.Blob(mime_type=doc_mime_type, data=doc_data)),
        ],
    )

    response = execute_user_query(
        runner_instance=runner_instance,
        user_id=user_id,
        session_id=session_id,
        user_content=user_content,
    )

    return str(response)
