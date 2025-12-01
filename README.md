# Story Crafter Agent

Transforms classic literature into personalized, illustrated stories adapted for different audiences using Google's Agent Development Kit (ADK).

## Problem & Solution

Classic literature contains timeless stories but faces modern challenges:
- Dense Victorian prose makes stories inaccessible
- Same text given to all age groups without adaptation
- Visual engagement expected by modern readers
- Significant time investment to read full texts

**Solution**: Multi-agent system that personalizes classics by adapting vocabulary, tone, length, and adding AI-generated illustrations while preserving core themes.

## Architecture

10-agent system with nested Sequential and Loop workflows:

```
StoryCrafterAgent (Root Orchestrator)
├── LibraryAgent (Book discovery)
├── PersonalizationAgent (User preferences)
└── StoryCreationPipeline (SequentialAgent)
    ├── RobustStoryGenerator (LoopAgent - max 2 iterations)
    │   ├── StoryTellerAgent (Story generation)
    │   └── QualityCheckerAgent (Quality validation)
    ├── IllustrationAgent (Image generation)
    └── FormatterAgent (Output formatting)
```

## Key Features

1. **10-agent orchestration** with nested workflow patterns
2. **Quality-driven generation** with objective validation metrics
3. **Personalized storytelling** for different ages and preferences
4. **AI-generated illustrations** with Airbrush.ai integration
5. **File-based memory** with 5 pre-cached classic books
6. **Graceful error handling** for external API failures
7. **Tool-based control flow** for dynamic agent behavior
8. **Production-quality output** as formatted markdown
9. **Offline capability** with pre-cached book data
10. **Bounded execution** with configurable iteration limits

## Technical Stack

- **Framework**: Google Agent Development Kit (ADK)
- **LLM Models**: Gemini 2.0 Flash (orchestration), Gemini 2.5 Pro (storytelling)
- **Agent Patterns**: SequentialAgent, LoopAgent, nested workflows
- **Image Generation**: Airbrush.ai API (optional)
- **Memory**: File-based caching with JSON
- **Runtime**: FastAPI with uvicorn
- **Python**: 3.10+

## Project Structure

```
story_crafter_agent/
├── __init__.py                 # Package initialization
├── agent.py                    # Root StoryCrafterAgent orchestrator
├── fast_api_app.py             # FastAPI web service
├── sub_agents/                 # Domain-specific agents
│   ├── library_agent.py        # Book discovery
│   ├── personalization_agent.py # User preferences
│   ├── storyteller_agent.py    # Story generation
│   ├── illustration_agent.py   # Image generation
│   └── formatter_agent.py      # Output formatting
├── tools/                      # Custom tools
│   ├── library_tools.py
│   ├── personalization_tools.py
│   ├── storyteller_tools.py
│   ├── image_generation_tools.py
│   └── formatting_tools.py
├── prompts/                    # Agent system prompts
│   ├── root_agent_mvp.md
│   ├── storyteller_agent.md
│   └── formatter_agent.md
└── cache/                      # Pre-cached data
    ├── books/                  # Classic book texts
    └── exports/                # Generated exports
```

## Installation

### Prerequisites
- Python 3.10+
- Google API Key (for Gemini models)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/story-crafter-agent.git
cd story-crafter-agent

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Quick Start

### Using Python

```python
from google.adk.runners import InMemoryRunner
from story_crafter_agent.agent import root_agent

runner = InMemoryRunner(agent=root_agent)
events = await runner.run_debug("Show me available books")
```

### Using FastAPI

```bash
python -m story_crafter_agent.fast_api_app
# Visit http://localhost:8086/docs
```

## Environment Variables

Create a `.env` file with:

```env
# Required - Choose ONE authentication method:

# Option 1: Gemini API (free tier, rate limited)
GOOGLE_API_KEY=your-gemini-api-key

# Option 2: Vertex AI (paid quota, recommended for production)
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Optional - image generation
AIRBRUSH_API_KEY=your-airbrush-key
AIRBRUSH_BASE_URL=https://api.airbrush.ai
```

**Note**: If you experience `429 RESOURCE_EXHAUSTED` errors with Vertex AI, see [`VERTEX_AI_SETUP.md`](VERTEX_AI_SETUP.md) for configuration troubleshooting.

## Workflow Execution Example

1. **StoryCrafterAgent** greets user and coordinates workflow
2. **LibraryAgent** lists 5 available classic books
3. **PersonalizationAgent** collects user preferences:
   - Target audience (age group)
   - Tone (whimsical, serious, etc.)
   - Length preference (short, medium, long)
   - Originality level (0.0-1.0)
4. **StoryCreationPipeline** executes sequentially:
   - RobustStoryGenerator (LoopAgent) with quality validation
   - IllustrationAgent generates images for story sections
   - FormatterAgent formats output as markdown
5. Final story saved with timestamp

## Data

Includes 5 pre-cached classic books:
1. **Moby-Dick** by Herman Melville (Adventure)
2. **Pride and Prejudice** by Jane Austen (Romance)
3. **Alice's Adventures in Wonderland** by Lewis Carroll (Fantasy)
4. **Frankenstein** by Mary Shelley (Gothic Horror)
5. **The Adventures of Sherlock Holmes** by Arthur Conan Doyle (Mystery)

## Development

### Running Tests
```bash
pytest story_crafter_agent/tests/
```

### Building Distribution
```bash
pip install build
python -m build
```

## ADK Features Demonstrated

- Multi-agent orchestration with 10 specialized agents
- Sequential workflow for ordered execution
- Loop workflow with quality-based exit conditions
- Nested workflows (Sequential + Loop)
- Tool context integration for dynamic control
- Custom domain-specific tools
- External API integration via MCP
- Long-term memory via file-based caching
- Error resilience with graceful degradation
- Bounded execution with configurable limits

## Future Directions

- Parallel agent patterns for concurrent processing
- Session management for extended interactions
- Context optimization for longer conversations
- Expanded book library from Project Gutenberg
- Multi-language support
- Audio narration capability
- Web UI for interactive story creation

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Apache License 2.0 - See LICENSE file for details

## Authors

Built with Google Agent Development Kit (ADK)

## Links

- [Google ADK Documentation](https://github.com/google-adk/python)
- [Gemini API Documentation](https://ai.google.dev)
