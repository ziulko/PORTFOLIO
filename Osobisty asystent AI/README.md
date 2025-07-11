# Personal AI Assistant (Private, Local, Context-Aware)

**A fully local, privacy-focused chatbot powered by LLMs (Large Language Models).**  
It remembers previous interactions, responds in Polish, and is designed to serve as your personal AI assistant — all without sending your data to the cloud.

---

## Key Features

- Local LLM integration via [Ollama](https://ollama.com/)
- Conversational memory (context-aware)
- Custom knowledge base from local documents (PDFs, notes, etc.)
- Web search tools (DuckDuckGo, Wikipedia, etc.)
- Streamlit or Gradio-based UI
- REST API for integration with external apps or websites
- Secure command layer for system/network diagnostics (research feature)

---

## Project Purpose & Research Scope

This project is also being developed as part of a master's thesis and will include a unique, security-oriented feature:

> _"An interactive system for data insight & diagnostics via language interface"_  
> _– built **into this assistant**, to support internal network visibility and analysis._

Planned capabilities specific to this use case:

-  **Trusted LLM interface for internal diagnostics**  
  (e.g. “check network interfaces”, “show firewall status”, “run ping to 8.8.8.8”)
- **Sandboxed and auditable** command execution (read-only or trusted tools only)
- **REST API** to enable interaction from external dashboards or scripts

This turns the assistant into a **secure, human-friendly interface for internal system introspection**.

---

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed

### Installation

```bash
git clone https://github.com/your-username/personal-ai-assistant.git
cd personal-ai-assistant

python3.10 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Running the Assistant

Make sure Ollama is running and a model is available:

```bash
ollama pull mistral
ollama run mistral  # keep this terminal running
```

Then launch the assistant:

```bash
python main.py
```

---

## Project Structure

```
personal-ai-assistant/
├── main.py                 ← Main chat interface
├── llm/
│   └── local_llm.py        ← LLM + memory + prompt logic
├── data/
│   └── knowledge_base/     ← Local documents for RAG (coming soon)
├── prompts/                ← Prompt templates
├── api/                    ← (Planned) REST interface for integration
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Roadmap

| Feature                             | Status   |
|------------------------------------|----------|
| Local LLM integration              |  Complete |
| Contextual memory                  |  Complete |
| Custom knowledge (PDFs, docs)      |  In progress |
| Web search tools                   |  In progress |
| Streamlit/Gradio frontend          |  Planned |
| API for external tools             |  Planned |
| Command/tool layer (diagnostics)   |  Planned |
| Thesis documentation integration   |  Planned |

---

## License

MIT © 2025 Jakub Z.

---

> **Disclaimer**: This project is an experimental AI assistant meant to run fully locally. It's under active development and will be extended as part of academic research.
