# Research Agent: process flows

## Domain request

Endpoint: `POST /agent/run`. Stages summarize [src/research/agent.py](../src/research/agent.py). This is in-process Python, not a hosted model or production apply.

```mermaid
flowchart TD
  A["POST /agent/run"] --> B{"Valid input?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes: Non-empty goal without publish/tweet/email"| C["Domain function in agent.py"]
  C --> O["note overlap hits; wrote false"]
  O --> X["No production side effect"]
```

See [INTERVIEW_QA.md](../INTERVIEW_QA.md) for fixture walkthroughs and [PROJECT_ARCHITECTURE.md](../PROJECT_ARCHITECTURE.md) for the component map.
