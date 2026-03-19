# Release Notes

## v0.2.0 - 2026-03-18

### Highlights

- Migrated the chatbot from OpenAI-backed inference to a local Ollama workflow.
- Updated the default local model to `gemma3:4b` for better responsiveness on CPU-only machines.
- Upgraded the project to target Python `3.14.3`.
- Simplified retrieval by replacing embedding-based search with BM25 retrieval over the local FAQ corpus.

### Added

- Added support for local Ollama configuration through `OLLAMA_BASE_URL` and `LANGUAGE_MODEL`.
- Added `watchdog` to improve Streamlit file watching in development.
- Added a `.python-version` file for consistent local Python setup.
- Added friendly runtime error handling when Ollama is unavailable or cannot load a model.

### Changed

- Replaced OpenAI chat and embedding integrations with a local Ollama chat integration.
- Switched retrieval from embedding-driven vector search to `BM25Retriever`.
- Updated document chunking to use `RecursiveCharacterTextSplitter` with overlapping chunks.
- Updated Streamlit and supporting dependencies for Python 3.14 compatibility.
- Changed the default local model from Qwen variants to `gemma3:4b`.
- Updated Docker to use `python:3.14-slim`.
- Updated Docker Compose to pass `OLLAMA_BASE_URL` through to app containers.
- Updated the README to match the current assistant prompt, retrieval flow, setup steps, and model defaults.

### Fixed

- Fixed Streamlit crashes by surfacing model-load and connection issues as readable app errors.
- Removed chunking warnings caused by the older fixed-width splitter setup.
- Removed the dependency on a separately loaded embedding model for the current FAQ use case.

### Notes

- The app is optimized for a small, local FAQ-style corpus and a single local Ollama chat model.
- On CPU-only systems, first-token latency may still be noticeable depending on the selected model.
- Python 3.14 still emits a LangChain/Pydantic deprecation warning in this stack, but the app runs successfully.
