
# GitHub Engineering Assistant

A backend-first portfolio project demonstrating production-style backend engineering: a Spring Boot GraphQL gateway and a FastAPI AI analysis service, using PostgreSQL for persistence and ChromaDB as a vector store. The project emphasizes architecture, testing, Dockerization, and a small AI/RAG feature.

## Architecture (ASCII)

```
Client (GraphQL Playground / Frontend)
                             |
       [Spring Boot :8080]  <-- GraphQL API (resolvers -> services -> repos / FastAPI client)
                             |
       [PostgreSQL :5432]  <-- Shared persistent store (repositories, analyses)
                             |
       [FastAPI :8000]     <-- AI Analysis + RAG (embeddings, ChromaDB, LLM)
                             |
       [ChromaDB :8001]    <-- Vector store (collection: github-repositories)
```

Goals:
- Clean separation of concerns: GraphQL for client-facing API and orchestration, FastAPI for AI and RAG pipelines.
- Production-like practices: async DB access, Alembic migrations, Docker Compose, JWT-ready structure, and tests.

Note: Run tests inside CI or with a local test DB; the project includes `tests/` and `scripts/generate_env.*` helpers.

---

## GraphQL example queries (copy-paste into GraphQL Playground)

# 1) Add a repository (calls FastAPI under the hood)
mutation AddRepo {
       addRepository(githubUrl: "https://github.com/octocat/Hello-World") {
              id
              githubUrl
              name
              description
              createdAt
       }
}

# 2) List repositories (with optional language filter)
query ListRepos {
       listRepositories(language: "Python", limit: 10) {
              id
              name
              language
              stars
       }
}

# 3) Trigger analysis for a repository
mutation TriggerAnalysis {
       triggerAnalysis(repositoryId: "PUT_REPO_ID_HERE") {
              id
              summary
              complexityScore
              topics
              createdAt
       }
}

# 4) Fetch analysis by repository (via GraphQL)
query GetAnalysis($repoId: ID!) {
       getAnalysis(repositoryId: $repoId) {
              id
              summary
              complexityScore
              topics
       }
}

---

## API endpoints (FastAPI)
- `POST /api/repositories` — register a repository for analysis (stores repo metadata)
- `GET /api/repositories` — list repositories
- `GET /api/repositories/{id}` — get repository details
- `POST /api/analyze/{id}` — trigger analysis (runs in background, returns current/queued state)
- `GET /api/search?query=...` — vector-search over analyzed content (returns matched IDs/metadata)

---

## Design decisions (explain each choice)

- **FastAPI (Python)**: chosen for its excellent async support, first-class Pydantic validation, and strong ML ecosystem (sentence-transformers, OpenAI SDK, httpx). FastAPI is a pragmatic choice for the AI analysis service because it allows straightforward integration with Python ML libraries and async I/O when calling the GitHub API and vector store.

- **Spring Boot (Java) + GraphQL**: used as the client-facing API to demonstrate a production-style, typed, enterprise-grade GraphQL gateway. Spring's GraphQL support and type safety make it a realistic choice for companies using Java stacks (such as Intuit). The service delegates domain logic and data access to service/repository layers and calls FastAPI for analysis tasks.

- **PostgreSQL**: reliable relational datastore for repository metadata and analysis results. Using a single shared SQL DB showcases realistic patterns for cross-service read models and enforces schema evolution with Alembic.

- **SQLAlchemy Async + Alembic**: async ORM to keep FastAPI fully async; Alembic for deterministic schema migrations. Separating `crud` and `usecases` implements a repository pattern and keeps business logic testable.

- **ChromaDB**: lightweight, easy-to-run vector store for embeddings. The project uses Chroma for local vector similarity without heavy infra dependencies. The collection name is `github-repositories`.

- **sentence-transformers (all-MiniLM-L6-v2)**: compact, fast embeddings suitable for small-scale RAG and demo purposes. Embeddings are generated in the FastAPI service and upserted into Chroma.

- **OpenAI / LLM stub**: the code supports calling OpenAI when `OPENAI_API_KEY` is present, otherwise falls back to a deterministic stub for reproducible behavior during development/testing.

- **Docker Compose**: single-command local orchestration for all services (Postgres, FastAPI, Spring, Chroma). Each service has healthchecks and named volumes for stateful persistence.

- **Testing strategy**: use Pytest with fixtures that create an async test DB or run tests inside containers. External calls (GitHub, OpenAI) should be mocked in tests. The CI runs unit tests for FastAPI and builds the Spring service.

---

If you'd like, I can now generate a polished `docs/architecture.md` with interview talking points and add the CI workflow file. (I'll add both next if you confirm.)
