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

#### 🔁 1. Sequential Spans
These are spans that happen one after another within the same service or thread.

Example:
```
[Span A] → [Span B] → [Span C]
```
Span A completes before Span B starts.

UI View (Timeline):
```
|--- Span A ----|
               |--- Span B ----|
                             |--- Span C ---|
```
#### 🧱 2. Nested Spans (Parent-Child Relationship)
This is the most common structure in distributed tracing. A parent span wraps around one or more child spans , which represent sub-operations.
```
[Parent Span: handle_request]
   ├── [Child Span: validate_token]
   └── [Child Span: fetch_user_data]
       └── [Grandchild Span: query_database]
```
- Child spans are logically part of their parent.
- Parent duration usually includes child durations (but not always if async).

UI View (Hierarchical Timeline):
```
|================= Parent Span ===================|
  |--- validate_token ---|
                          |===== fetch_user_data ======|
                                      |--- query_database ---|
```
This nesting shows that fetch_user_data happened during the handle_request, and inside it, a database query was made.
#### ⏱️ 3. Concurrent / Parallel Spans
Multiple child spans can run in parallel , especially when a service makes multiple downstream calls at once.
```
[Parent Span: generate_report]
   ├── [Child Span: fetch_sales_data]
   ├── [Child Span: fetch_inventory_data]
   └── [Child Span: fetch_user_data]
```
All three child spans start around the same time and may finish at different times.

```
|=============== Parent Span ===============|
  |-- fetch_sales --|
  |---- fetch_inventory ----|
  |------ fetch_users ------|
```
### Timeline View
The Jaeger UI displays all the spans in a timeline view , showing:
- The duration of each span
- Parent-child relationships between spans
- Concurrent vs sequential operations

This allows you to:
- See which service took the most time
- Identify parallelizable steps
- Detect delays or slow calls

### Error Flags & Logs
If any span encountered an error:
- It may be marked with an error tag
- You can inspect logs within the span to see what went wrong
```
error=true
http.status_code=500
```
## Example using OTLP SDK
```
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```
The code
```python
import time
import random
from datetime import timedelta
from opentelemetry import trace, context
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode


# Setup OpenTelemetry with OTLP (Grafana Alloy)
def configure_tracer():
    resource = Resource(attributes={
        "service.name": "simple-python-service",
        "environment": "testing",
        "version": "1.0.0"
    })

    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Configure OTLP Exporter (Grafana Alloy)
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    return trace.get_tracer(__name__)


tracer = configure_tracer()


# Simulated function 1: Main entry point
@tracer.start_as_current_span("main")
def main():
    span = trace.get_current_span()

    # 🔖 Add tags (attributes)
    span.set_attribute("user.id", "12345")
    span.set_attribute("operation.type", "request")

    print("Starting main operation...")
    time.sleep(random.uniform(0.05, 0.1))  # Simulate processing delay

    # 📝 Add an event (log-like annotation)
    span.add_event("User request started", {"http.method": "GET", "http.path": "/api/data"})

    try:
        authenticate_user()
        span.set_status(Status(StatusCode.OK))
    except Exception as e:
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR, description=str(e)))
        span.add_event("Error occurred", {"exception.message": str(e)})


# Simulated function 2: Authentication step
@tracer.start_as_current_span("authenticate_user")
def authenticate_user():
    span = trace.get_current_span()

    span.set_attribute("auth.method", "bearer_token")
    span.set_attribute("auth.user", "demo_user")

    print("Authenticating user...")
    time.sleep(random.uniform(0.05, 0.1))  # Simulate auth delay

    span.add_event("Authentication successful", {
        "auth.scopes": ["read", "write"],
        "auth.expires_in": str(timedelta(minutes=30))
    })

    fetch_data()


# Simulated function 3: Data fetching step
@tracer.start_as_current_span("fetch_data")
def fetch_data():
    span = trace.get_current_span()

    span.set_attribute("db.type", "postgresql")
    span.set_attribute("db.query_type", "SELECT")

    print("Fetching data from backend...")
    time.sleep(random.uniform(0.05, 0.1))  # Simulate DB or API call

    span.add_event("Database query executed", {
        "db.statement": "SELECT * FROM users WHERE id = '12345'",
        "db.rows_returned": 1
    })


if __name__ == "__main__":
    for i in range(3):  # Run a few times to see multiple traces
        print(f"\n--- Request {i + 1} ---")
        try:
            main()
        except Exception as e:
            print(f"Error in request {i+1}: {e}")
```
### How does a trace begin
#### ✨ The First Span Starts the Trace
A trace starts when the first span is created — usually at the entry point of your service (e.g., an HTTP request, a message queue consumer, or a CLI command).
```
@tracer.start_as_current_span("main")
def main():
    ...
```
Here, main() is the root span , so:
- A new Trace ID is generated.
- This span becomes the parent of any subsequent spans (like authenticate_user and fetch_data).
- It's also marked as the current span in the execution context.
- So the trace begins when main() starts.
#### 2️⃣ How Are Child Spans Linked?
Each time you create a new span inside another span, OpenTelemetry automatically links them using context propagation.
```
@tracer.start_as_current_span("authenticate_user")
def authenticate_user():
    ...
```
Under the hood, this does:
- Looks for the current active span (main)
- Creates a new span (authenticate_user) with:
- Same Trace ID
- New Span ID
- Reference to the parent span via parent_span_id
- Makes authenticate_user the current span temporarily
So now the structure looks like:
```
[main] ← root span
 └── [authenticate_user]
     └── [fetch_data]
```
This builds the hierarchical tree of operations that you see in Grafana or Jaeger.
#### 3️⃣ How Does a Trace End?
✅ When the Root Span Ends

The trace ends when the root span ends.
```
@tracer.start_as_current_span("main")
def main():
    ...
```
When main() finishes, the span is closed (OpenTelemetry handles this via the decorator), and the full trace is exported.

Behind the scenes:
- The span records its end timestamp
- All child spans must already be finished (or they are orphaned)
- The completed trace is queued for export (to Alloy, Jaeger, etc.)
#### 4️⃣ What Is the "Trace Context"?
Trace ID
Unique ID shared by all spans in the same trace

Span ID
Unique ID for this specific span

Trace Flags
E.g., whether the trace should be sampled

Trace State
Optional metadata (e.g., tenant, region)

#### 5️⃣ How Is Context Passed Between Services?
This is called distributed context propagation .

Example: main() calls an external API → how does the next service know it's part of the same trace?

OpenTelemetry supports protocols like:

- HTTP Headers :
```
traceparent: 00-abc123... (Trace ID)-def456... (Span ID)-01
```
- Message headers (for Kafka, RabbitMQ, etc.)
- gRPC metadata
When the downstream service receives the request, it extracts the trace context and creates a new span with the correct parent.
