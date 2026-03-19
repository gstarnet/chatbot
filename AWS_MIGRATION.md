# AWS Migration Plan

## Purpose

This document describes how to migrate this repository from a local proof of concept into a production-ready AWS deployment.

The current codebase is a lightweight local application that uses:

- Streamlit for the user interface
- LangChain for prompt orchestration
- BM25 retrieval over a local FAQ file
- a local Ollama runtime for model inference

That is a good proof of concept, but it is not yet shaped for a cloud-native AWS production environment.

This document covers:

- the recommended AWS target architecture
- when Bedrock is the best fit
- when SageMaker is the better fit
- how vector search fits into AWS production
- how to move from one local FAQ file to multi-document search
- a phased migration path from the current repository

## Current State

The current request flow is:

1. Streamlit receives a user question.
2. The app loads a local FAQ text file.
3. The file is chunked in process.
4. BM25 retrieves matching chunks.
5. LangChain assembles the prompt.
6. A local Ollama model returns the answer.

This is intentionally simple, but it has the following limitations:

- no cloud deployment boundary
- no shared API service
- no document ingestion pipeline
- no object storage
- no database-backed metadata
- no authentication or authorization
- no tenant isolation
- no managed observability
- no scalable retrieval for many documents
- no AWS-native security or network controls

## Recommended AWS Target

For this repository, the best first AWS production target is:

- frontend UI
- FastAPI backend
- Amazon Bedrock for model inference
- Bedrock Knowledge Bases or PostgreSQL plus pgvector for retrieval
- Amazon RDS PostgreSQL for application data
- Amazon S3 for document storage
- Amazon ElastiCache Redis for cache and rate limiting
- CloudWatch and X-Ray or OpenTelemetry-based observability
- ECS or EKS for application deployment

This is the cleanest migration path because it keeps the application architecture under your control while offloading model operations to AWS-managed services.

## Bedrock vs SageMaker

This is the most important AWS platform decision for this project.

### Bedrock

Amazon Bedrock is the better fit when you want:

- managed foundation model inference
- low operational overhead
- fast time to production
- AWS-native RAG support
- model choice without building custom hosting infrastructure

Bedrock is well suited for this repository because the current app is a classic retrieval plus prompt plus inference pattern. That maps directly to Bedrock’s managed model APIs and Bedrock Knowledge Bases.

Bedrock is the recommended choice if:

- you are building a production application rather than a model platform
- you want to move off local inference quickly
- you want AWS to manage the model-serving layer
- you want an easier path to enterprise security and operations
- you expect retrieval-augmented generation to remain the core interaction pattern

### SageMaker

Amazon SageMaker is the better fit when you want:

- to host your own model endpoints
- custom inference containers
- fine-tuning pipelines
- advanced performance optimization
- full control over model runtime behavior

SageMaker is a stronger fit if your team is building model infrastructure rather than only an application layer.

SageMaker is the recommended choice if:

- you need to serve custom weights
- you need specialized GPU scheduling or scaling control
- you need custom inference logic
- you need deep model optimization or private model hosting patterns
- you want to own the full model-serving lifecycle

### Recommended Decision for This Repo

For this repository, Bedrock is the better first production choice.

Why:

- this project is currently an application, not a model platform
- the main challenge is productionizing retrieval, orchestration, and deployment
- managed inference is a better tradeoff than self-managed model hosting at this stage
- Bedrock reduces infrastructure burden and accelerates migration from the current local setup

SageMaker should only become the primary choice later if the project evolves into a custom model-serving platform or requires capabilities Bedrock does not provide.

## Best-Fit AWS Architecture

The recommended target architecture for this repository is:

1. Frontend sends a chat request.
2. API Gateway or Application Load Balancer routes traffic to the backend.
3. FastAPI backend handles authentication, session state, prompt orchestration, and retrieval.
4. Retrieval layer fetches relevant documents.
5. Prompt builder assembles system instructions and retrieved context.
6. Bedrock model inference generates the answer.
7. Backend stores conversation state, citations, and telemetry.
8. Response is returned to the client.

## Recommended AWS Service Mapping

### Application Layer

- Amazon ECS Fargate or Amazon EKS
  - deploy FastAPI backend
  - optionally deploy a separate internal admin UI
- Application Load Balancer
  - route HTTPS traffic to backend services
- Amazon API Gateway
  - optional, if you want a formal API edge layer

### Data Layer

- Amazon RDS for PostgreSQL
  - users
  - sessions
  - document metadata
  - access control
  - chat history
- Amazon ElastiCache for Redis
  - cache
  - rate limiting
  - short-lived state
- Amazon S3
  - source documents
  - upload staging
  - parsed artifacts

### Retrieval Layer

You have two good AWS paths:

#### Option A: Bedrock Knowledge Bases

Use this when you want the fastest path to managed RAG.

Benefits:

- managed ingestion and retrieval flow
- simpler first production release
- less platform work

Tradeoffs:

- less low-level control
- more service-level coupling to AWS managed RAG patterns

#### Option B: Your Own Retrieval Stack

Use this when you want more control.

Recommended stack:

- PostgreSQL for app state
- pgvector in PostgreSQL for semantic search
- BM25 or OpenSearch for keyword retrieval
- your own retrieval service in the backend

Benefits:

- more flexibility
- easier custom ranking logic
- better long-term portability

Tradeoffs:

- more engineering work
- more moving parts

## Recommended Retrieval Strategy on AWS

For production, retrieval should evolve in stages.

### Stage 1

Launch with BM25 or Bedrock Knowledge Bases if the document set is still modest.

This works well when:

- the corpus is still relatively small
- you are optimizing for simplicity
- you want the fastest path to production

### Stage 2

Move to hybrid retrieval.

Hybrid retrieval means:

- keyword retrieval for exact terms and structured phrases
- vector retrieval for semantic similarity
- optional reranking before prompt assembly

This becomes valuable when:

- document count grows
- wording varies more
- exact term matching is no longer enough

### Stage 3

Add document filtering and policy-aware retrieval.

Examples:

- tenant-aware search
- region-aware search
- access-controlled search
- version-aware retrieval

This is critical in real production systems.

## Multi-Document Migration on AWS

Moving from one FAQ file to a multi-document system is the most important functional change after basic productionization.

### What changes

Instead of reading one text file from disk, the system should:

- store source documents in S3
- register document metadata in PostgreSQL
- parse documents through an ingestion service
- split them into chunks
- attach metadata to each chunk
- index them into retrieval storage
- retrieve across all relevant documents at runtime

### Minimum document metadata model

You should store:

- document id
- tenant id
- title
- source location
- content type
- version
- tags
- status
- permissions
- created and updated timestamps

Chunk records should store:

- chunk id
- document id
- chunk index
- text
- metadata
- optional embedding reference

### Runtime retrieval flow for multi-document search

1. user asks a question
2. backend loads user and tenant context
3. backend filters eligible documents
4. retriever fetches candidate chunks
5. reranker optionally orders them
6. top chunks are inserted into the prompt
7. model responds with citations

## AWS Reference Architecture by Phase

### Phase 1: Move the App to an AWS Backend

Goal:

- stop treating Streamlit as the application runtime
- create a proper API backend

Changes:

- introduce FastAPI backend
- move LangChain flow into reusable service code
- deploy backend on ECS Fargate or EKS
- use ALB or API Gateway in front
- store sessions in PostgreSQL
- use S3 for file-backed content instead of local disk

Expected outcome:

- the app becomes deployable and scalable
- backend logic is no longer tied to a local UI process

### Phase 2: Replace Ollama with Bedrock

Goal:

- remove local model hosting from the production path

Changes:

- replace direct local model calls with a Bedrock-backed model adapter
- keep application-side prompt assembly under your control
- add model configuration through environment settings
- add request timeout, retry, and fallback handling

Expected outcome:

- model operations become AWS-managed
- production reliability improves significantly

### Phase 3: Add Multi-Document Ingestion

Goal:

- move from one FAQ file to a real document corpus

Changes:

- add S3-based document upload or sync
- build ingestion workers
- parse and chunk documents
- store metadata in PostgreSQL
- register searchable chunks

Expected outcome:

- the app can answer from many documents
- content updates no longer require code changes

### Phase 4: Add Managed or Hybrid Retrieval

Goal:

- improve retrieval quality and scale

Choices:

- Bedrock Knowledge Bases for faster managed RAG
- PostgreSQL plus pgvector for a more custom stack
- OpenSearch if search becomes a dedicated concern

Expected outcome:

- better retrieval quality
- easier support for larger and more diverse corpora

### Phase 5: Harden for Enterprise Production

Goal:

- make the system secure, observable, and maintainable

Changes:

- AWS IAM integration
- Cognito or enterprise identity integration
- document-level permissions
- CloudWatch dashboards and alarms
- distributed tracing
- WAF and rate limiting
- audit logging
- CI/CD pipelines
- blue/green or canary deployment support

Expected outcome:

- operationally stable system
- secure access model
- clearer incident response and release management

## Recommended Deployment Choices

### ECS Fargate vs EKS

For this repository, ECS Fargate is the better first production choice.

Why:

- lower operational burden
- easier onboarding for an app-focused team
- enough flexibility for the likely first production release

Choose EKS only if:

- your organization already runs Kubernetes
- you need tighter control over platform architecture
- you expect to operate multiple related services at larger scale

## Bedrock Knowledge Bases vs Custom Retrieval

### Choose Bedrock Knowledge Bases if

- you want the fastest AWS-native RAG path
- you accept managed retrieval patterns
- you want less infrastructure to own

### Choose custom retrieval if

- you want hybrid search on your own terms
- you need custom ranking logic
- you want more portability
- retrieval quality is central to the product

## Recommended First AWS Production Version

For this repository, the best first AWS production version is:

- FastAPI backend on ECS Fargate
- ALB in front of the service
- Bedrock for inference
- PostgreSQL on RDS
- Redis on ElastiCache
- S3 for document storage
- BM25 or Bedrock Knowledge Bases for initial retrieval
- CloudWatch for logs and alarms

This is the best balance of speed, maintainability, and production readiness.

## When to Revisit SageMaker

You should revisit SageMaker if:

- you need custom hosted models
- you need fine-tuning pipelines
- you need lower-level control of inference
- model infrastructure becomes a core competency of the team

Until then, Bedrock is the more appropriate service choice for this application.

## Risks and Tradeoffs

### Bedrock Risks

- higher usage-based costs than small local setups
- more AWS service coupling
- less low-level runtime control

### SageMaker Risks

- more infrastructure and MLOps burden
- higher operational complexity
- slower migration path from the current codebase

### Recommendation

Start with Bedrock.

Only move to SageMaker if product requirements clearly demand custom model hosting or model lifecycle ownership.

## Migration Checklist

- extract chatbot logic into a backend service
- deploy backend on ECS Fargate
- move documents to S3
- move metadata and sessions to RDS PostgreSQL
- add Redis
- replace Ollama adapter with Bedrock adapter
- add ingestion workers
- support multiple documents and citations
- choose Bedrock Knowledge Bases or custom retrieval
- add auth and policy-aware retrieval
- add monitoring, tracing, and alerting
- add CI/CD and release automation

## Summary

The best AWS production migration path for this repository is to treat it as an application modernization effort, not a model-hosting project.

That means:

- move the app into a real backend service
- shift inference to Bedrock
- move content into S3 and PostgreSQL-backed metadata
- support multi-document retrieval
- add observability and security

Bedrock is the better first fit because it lets the team focus on application architecture, retrieval quality, and production reliability instead of self-managing model infrastructure.

SageMaker becomes the better fit only when the project needs custom model hosting, fine-tuning, or deeper model-serving control.
