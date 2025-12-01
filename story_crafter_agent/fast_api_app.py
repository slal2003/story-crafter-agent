# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Load environment variables FIRST, before any ADK imports
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

# Load .env from project root
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
else:
    # Fallback: try current directory
    load_dotenv(override=True)

# Verify Vertex AI configuration
use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").upper() in ("1", "TRUE", "YES", "Y")

print("\n" + "="*70)
print("◈ STORY CRAFTER AGENT - AUTHENTICATION CHECK")
print("="*70)

if use_vertex:
    print("✓ FastAPI: Using VERTEX AI backend (GOOGLE_GENAI_USE_VERTEXAI is set)")
    print("  Project:", os.getenv("GOOGLE_CLOUD_PROJECT", "Not set"))
    print("  Location:", os.getenv("GOOGLE_CLOUD_LOCATION", "Not set"))
    
    # Check which gcloud account is active
    try:
        import subprocess
        result = subprocess.run(
            ["gcloud", "config", "get-value", "account"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            account = result.stdout.strip()
            print(f"  Authenticated as: {account}")
        else:
            print(f"  Authenticated as: [Unable to determine - run: gcloud auth list]")
    except Exception as e:
        print(f"  Authenticated as: [Error checking: {str(e)[:50]}]")
else:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"⚠️ FastAPI: Using GEMINI API backend (FREE TIER - will hit 429 limits!)")
        print(f"  API Key loaded: {api_key[:20]}... ({len(api_key)} chars total)")
        print(f"  This will be rate-limited to 60 requests/minute!")
    else:
        print("❌ FastAPI: No authentication configured!")

print("="*70 + "\n")

from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

from story_crafter_agent.sub_agents.illustration_agent import illustration_agent
from story_crafter_agent.sub_agents.formatter_agent import formatter_agent
from story_crafter_agent.sub_agents.storyteller_agent import storyteller_agent
from story_crafter_agent.sub_agents.personalization_agent import personalization_agent

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create FastAPI app with ADK integration
# Note: We disable OpenAPI schema generation for complex types
app: FastAPI = get_fast_api_app(
    agents=[personalization_agent, storyteller_agent, illustration_agent, formatter_agent],
    web=True,
    allow_origins=["*"],  # Configure as needed for production
    session_service_uri=None,  # In-memory sessions
)

app.title = "Illustrated Summary Agent"
app.description = "ADK Agent for Personalized Illustrated Summaries of Classic Literature"

# Override OpenAPI schema to handle Pydantic validation issues
# This is a workaround for complex ADK types in the schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Return a simplified OpenAPI schema that documents the main endpoints
    # without triggering Pydantic validation errors on complex ADK types
    openapi_schema = {
        "openapi": "3.1.0",
        "info": {
            "title": app.title,
            "version": "0.1.0",
            "description": app.description + "\n\n**Note**: Full API documentation available via ADK. This is a simplified schema.",
        },
        "paths": {
            "/": {
                "get": {
                    "summary": "Root",
                    "description": "API root endpoint",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "Health Check",
                    "description": "Check if the service is healthy",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/sessions": {
                "post": {
                    "summary": "Create Session",
                    "description": "Create a new agent session",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "agent_id": {
                                            "type": "string",
                                            "description": "Agent ID (use 'app')"
                                        }
                                    },
                                    "required": ["agent_id"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Session created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "session_id": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/sessions/{session_id}/messages": {
                "post": {
                    "summary": "Send Message",
                    "description": "Send a message to the agent",
                    "parameters": [
                        {
                            "name": "session_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "content": {
                                            "type": "string",
                                            "description": "Message content"
                                        }
                                    },
                                    "required": ["content"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Message sent successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8086)

