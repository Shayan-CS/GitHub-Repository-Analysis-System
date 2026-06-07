# Architecture & Interview Talking Points

This document provides concise interview-style talking points for each major technology and design decision in the GitHub Engineering Assistant project.

## Spring Boot (GraphQL)

What it is
- Java-based framework for building production-grade REST/GraphQL services.

Why used here
- Provides a typed, enterprise-ready GraphQL gateway; aligns with hiring stacks that value Java/Spring.

Key implementation notes
- Controllers (resolvers) delegate to `service` layer; business logic is not in resolvers.
- Uses Spring Data JPA for read-only access against the shared Postgres DB.

Interview talking points
- Explain `@QueryMapping` and `@MutationMapping` and why resolvers should be thin.
- Discuss how you'd handle pagination, error mapping, and batching for GraphQL.

## GraphQL

What it is
- A query language and runtime for APIs, enabling clients to request exactly the data they need.

Why used here
- Simplifies frontend integrations by returning precise shapes; GraphQL Playground is useful for demos.

Interview talking points
- Explain schema design: types, queries, mutations and how to model relations (Repository -> Analysis).
- Explain trade-offs vs REST (caching complexity, overfetching vs underfetching).

## PostgreSQL

What it is
- Reliable relational database, used for persistent storage of repository and analysis records.

Why used here
- Strong ACID guarantees, array/JSON support for analysis `topics`, and wide industry adoption.

Interview talking points
- Explain normalization vs denormalization choices; why you might store analyses in a separate table.
- Discuss indexing strategies for common queries (e.g., index by `repository_id`, `language`, or `created_at`).

## FastAPI

What it is
- Modern Python ASGI framework with fast async support and Pydantic validation.

Why used here
- Best fit for integrating Python ML libraries, async I/O for GitHub and Chroma calls.

Interview talking points
- Describe dependency injection via `Depends` and startup/shutdown events used for DB engine lifecycle.
- Explain how Pydantic models become the API contract and auto-generate OpenAPI docs.

## Docker & Docker Compose

What they are
- Containers and local orchestration for multi-service applications.

Why used here
- Reproducible local environment for the entire stack: Postgres, FastAPI, Spring, Chroma.

Interview talking points
- Explain `depends_on` caveats (start vs healthy conditions) and healthchecks.
- Discuss volumes for stateful services and how to manage secrets (.env files vs secrets manager).

## RAG / Vector Search (ChromaDB + embeddings)

What it is
- Retrieval-Augmented Generation uses vector search (nearest neighbors on embeddings) to provide context to LLMs.

Why used here
- Allows repository-level Q&A and context-aware summaries without sending entire repo content to the model.

Interview talking points
- Explain embedding lifecycle: generate embeddings, upsert to vector store, query with embedding, retrieve passages.
- Discuss trade-offs: embedding model quality vs cost, vector store scaling, and freshness of indexes.

## Microservices design

What it is
- Split services by responsibility: GraphQL gateway vs AI analysis service.

Why used here
- Separation of concerns, language-appropriate tools (Java for GraphQL gateway, Python for AI), and independent scaling.

Interview talking points
- How would you handle shared DB consistency, cross-service transactions, and eventual consistency for analyses?
- How to implement authentication/authorization across services (JWT, API gateway), and rate-limiting for external API calls.

## Testing & CI considerations

What to emphasize
- Unit tests for business logic; integration tests for DB interactions; mock external HTTP/LLM calls.

CI pipeline talking points
- Run unit tests for FastAPI (pytest) and build Spring service (mvn package) in separate jobs.
- Possibly spin up a test Postgres and Chroma in CI (or use lightweight SQLite and mocks) for integration tests.

---

Use these bullets to prepare concise answers for interviews; you should be able to draw a simple diagram and walk through a request from client -> GraphQL -> service -> DB / FastAPI, and explain why the split exists, how data flows, and how you'd improve or scale the system.
