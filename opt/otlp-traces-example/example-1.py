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
