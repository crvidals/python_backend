import uuid
import json
from typing import Any
from openai import AsyncOpenAI
from app.core.config import get_settings
from app.ai.prompts.system import SYSTEM_PROMPT
from app.ai.tools.opportunity import get_opportunity_tools
from app.services.opportunity import OpportunityService
from app.database.repositories.opportunity import OpportunityRepository
from app.schemas.ai import AIChatRequest, AIChatResponse
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

conversation_memory: dict[str, list[dict[str, str]]] = {}


class AIService:
    def __init__(self, opportunity_service: OpportunityService):
        self.opportunity_service = opportunity_service
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.tools = get_opportunity_tools()

    async def _execute_tool(self, tool_call: dict[str, Any]) -> str:
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])

        if function_name == "search_opportunities":
            stage = arguments.get("stage")
            priority = arguments.get("priority")
            owner = arguments.get("owner")
            items, total = await self.opportunity_service.get_all(
                stage=stage, priority=priority, owner=owner, limit=50
            )
            results = [
                {
                    "name": item.opportunity_name,
                    "company": item.company_name,
                    "stage": item.stage,
                    "priority": item.priority,
                    "value": item.estimated_value,
                    "probability": item.probability,
                }
                for item in items
            ]
            return json.dumps({"opportunities": results, "total": total})

        elif function_name == "get_opportunity_summary":
            name = arguments.get("opportunity_name", "")
            items, _ = await self.opportunity_service.get_all(limit=100)
            for item in items:
                if item.opportunity_name.lower() == name.lower():
                    return json.dumps({
                        "name": item.opportunity_name,
                        "company": item.company_name,
                        "contact": item.contact_name,
                        "email": item.contact_email,
                        "stage": item.stage,
                        "priority": item.priority,
                        "value": item.estimated_value,
                        "currency": item.currency,
                        "probability": item.probability,
                        "description": item.description,
                        "ai_recommendation": item.ai_recommendation,
                    })
            return json.dumps({"error": f"Opportunity '{name}' not found"})

        elif function_name == "get_pipeline_stats":
            items, total = await self.opportunity_service.get_all(limit=200)
            stage_counts: dict[str, int] = {}
            total_value = 0.0
            for item in items:
                stage_counts[item.stage] = stage_counts.get(item.stage, 0) + 1
                if item.estimated_value:
                    total_value += item.estimated_value
            return json.dumps({
                "total_opportunities": total,
                "by_stage": stage_counts,
                "total_estimated_value": total_value,
            })

        return json.dumps({"error": f"Unknown tool: {function_name}"})

    async def chat(self, request: AIChatRequest) -> AIChatResponse:
        conversation_id = request.conversation_id or str(uuid.uuid4())

        if conversation_id not in conversation_memory:
            conversation_memory[conversation_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]

        conversation_memory[conversation_id].append({"role": "user", "content": request.question})

        messages = conversation_memory[conversation_id]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
            )

            choice = response.choices[0]
            message = choice.message

            if message.tool_calls:
                tool_messages = []
                for tool_call in message.tool_calls:
                    result = await self._execute_tool(tool_call)
                    tool_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

                conversation_memory[conversation_id].append(message.model_dump())
                conversation_memory[conversation_id].extend(tool_messages)

                second_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation_memory[conversation_id],
                )

                answer = second_response.choices[0].message.content or "No pude generar una respuesta."
                conversation_memory[conversation_id].append({"role": "assistant", "content": answer})
            else:
                answer = message.content or "No pude generar una respuesta."
                conversation_memory[conversation_id].append({"role": "assistant", "content": answer})

        except Exception as e:
            logger.error(f"AI service error: {str(e)}")
            answer = "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente."

        return AIChatResponse(
            answer=answer,
            conversation_id=conversation_id,
        )
