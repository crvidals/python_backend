from typing import Any


def get_opportunity_tools() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "search_opportunities",
                "description": "Buscar oportunidades comerciales por criterios específicos",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "stage": {
                            "type": "string",
                            "description": "Etapa de la oportunidad",
                            "enum": ["Lead nuevo", "Contactado", "Diagnóstico", "Propuesta enviada", "Negociación", "Ganado", "Perdido"]
                        },
                        "priority": {
                            "type": "string",
                            "description": "Prioridad de la oportunidad",
                            "enum": ["Baja", "Media", "Alta", "Crítica"]
                        },
                        "owner": {
                            "type": "string",
                            "description": "Responsable de la oportunidad"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_opportunity_summary",
                "description": "Obtener un resumen detallado de una oportunidad específica",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "opportunity_name": {
                            "type": "string",
                            "description": "Nombre de la oportunidad"
                        }
                    },
                    "required": ["opportunity_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_pipeline_stats",
                "description": "Obtener estadísticas del pipeline de ventas",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]
