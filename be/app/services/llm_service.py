import json
import logging

from typing import AsyncGenerator
from google import genai
from google.genai import types
from fastapi import HTTPException
from pydantic import BaseModel

from app.config import settings
from app.models.request import GenerateBatchRequest
from app.models.response import GenerateBatchResponse, Scenario, Choice
from app.prompts.scenario_prompt import SYSTEM_PROMPT, build_user_message

logger = logging.getLogger(__name__)

# Configure Gemini client
client = genai.Client(api_key=settings.LLM_API_KEY)

MAX_RETRIES = 2


class ScenariosOutput(BaseModel):
    """Schema for structured output from Gemini API."""
    scenarios: list[Scenario]


async def generate_scenarios(request: GenerateBatchRequest) -> GenerateBatchResponse:
    """Generate a batch of scenarios by calling the Gemini LLM API.

    Uses Gemini structured output to get validated JSON directly.
    Retries up to MAX_RETRIES times on failure.
    Raises HTTP 422 if all retries fail.
    """
    user_message = build_user_message(
        name=request.child.name,
        age=request.child.age,
        location=request.child.location,
        notes=request.child.notes,
        total=request.config.total,
        difficulty=request.config.difficulty,
        max_difficulty=settings.MAX_DIFFICULTY,
    )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"LLM call attempt {attempt}/{MAX_RETRIES}")
            response = client.models.generate_content(
                model=settings.LLM_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=ScenariosOutput,
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=0,
                    ),
                ),
            )

            parsed: ScenariosOutput = response.parsed

            return GenerateBatchResponse(
                scenarios=parsed.scenarios,
            )

        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt} failed: {e}")
            continue

    raise HTTPException(
        status_code=422,
        detail=f"Failed to generate valid scenarios after {MAX_RETRIES} attempts: {last_error}",
    )


def find_matching_brace(s: str, start_idx: int) -> int:
    """Find the index of the matching closing brace for the one at start_idx."""
    count = 0
    in_string = False
    escape = False
    for i in range(start_idx, len(s)):
        char = s[i]
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"':
            if i > 0 and s[i - 1] == '\\':
                # Check if the backslash itself is escaped
                backslashes = 0
                for j in range(i - 1, -1, -1):
                    if s[j] == '\\':
                        backslashes += 1
                    else:
                        break
                if backslashes % 2 == 1:
                    # Escaped quote
                    continue
            in_string = not in_string
            continue
        if not in_string:
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
                if count == 0:
                    return i
    return -1


async def stream_generate_scenarios(request: GenerateBatchRequest) -> AsyncGenerator[str, None]:
    """Stream scenario generation from Gemini.

    Yields scenario objects as Server-Sent Events (SSE).
    """
    user_message = build_user_message(
        name=request.child.name,
        age=request.child.age,
        location=request.child.location,
        notes=request.child.notes,
        total=request.config.total,
        difficulty=request.config.difficulty,
        max_difficulty=settings.MAX_DIFFICULTY,
    )

    try:
        logger.info("Starting LLM streaming call (async)")
        # Use client.aio for true async streaming
        response = await client.aio.models.generate_content_stream(
            model=settings.LLM_MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ScenariosOutput,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0,
                ),
            ),
        )

        buffer = ""
        in_scenarios_list = False

        async for chunk in response:
            if chunk.text:
                buffer += chunk.text

                # If we haven't found the start of the scenarios list yet
                if not in_scenarios_list:
                    if '"scenarios":' in buffer and '[' in buffer:
                        start_of_list = buffer.find('[')
                        buffer = buffer[start_of_list + 1:]
                        in_scenarios_list = True
                    else:
                        # Haven't reached the list yet
                        continue

                # Try to extract objects from the buffer
                while True:
                    start_idx = buffer.find('{')
                    if start_idx == -1:
                        break

                    end_idx = find_matching_brace(buffer, start_idx)
                    if end_idx == -1:
                        break

                    # We have a potential object
                    obj_str = buffer[start_idx : end_idx + 1]
                    try:
                        obj = json.loads(obj_str)
                        # Yield in SSE format
                        yield f"event: scenario\ndata: {json.dumps(obj, ensure_ascii=False)}\n\n"
                        
                        # Remove processed part and move on
                        buffer = buffer[end_idx + 1:]
                        buffer = buffer.lstrip(', \n\r\t')
                    except json.JSONDecodeError:
                        # Not a full object yet, wait for more chunks
                        break

        # Final event to signify completion
        yield "event: done\ndata: {}\n\n"

    except Exception as e:
        logger.error(f"Streaming attempt failed: {e}")
        yield f"event: error\ndata: {json.dumps({'detail': str(e)}, ensure_ascii=False)}\n\n"
