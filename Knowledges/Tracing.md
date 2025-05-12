# Distributed tracing
In Jaeger , a trace is a representation of a transaction or operation that has been routed through multiple services (or calls) in a distributed system. 

It helps you understand the flow of requests , latency breakdowns , and potential bottlenecks .

### 🔍 What a Trace Consists of (in Jaeger)
When browsing traces in Jaeger, each trace consists of the following key components:

1. Trace ID
- A globally unique identifier for the entire trace.
- All spans related to the same request share this ID.
2. Spans
- A span represents a logical unit of work in executing a distributed operation. Each span includes:

### 📦 Span Structure:
- Span ID : Unique identifier for the span.
- Operation Name : The name of the operation (e.g., GET /api/users, rpc call, db query).
- Start Time and Duration : When the span started and how long it lasted.
- Tags (Key-Value Metadata) : Arbitrary metadata about the operation (e.g., HTTP status code, error flags).
- Logs (Optional Events within a Span) : Timestamped events recorded inside a span (e.g., "User not found", "Retrying connection").
References to Other Spans :
- Parent Span ID : Used to form the hierarchical structure of the trace.
- Types of references: CHILD_OF, FOLLOWS_FROM (for causal relationships).
