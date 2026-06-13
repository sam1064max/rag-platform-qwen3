from langfuse import Langfuse
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(
    service_name: str = "rag-platform-qwen3",
    otel_endpoint: str = "http://localhost:4317",
    langfuse_public_key: str = "",
    langfuse_secret_key: str = "",
    langfuse_host: str = "http://localhost:3000",
) -> trace.Tracer:
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "1.0.0",
        }
    )

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    if langfuse_public_key and langfuse_secret_key:
        Langfuse(
            public_key=langfuse_public_key,
            secret_key=langfuse_secret_key,
            host=langfuse_host,
        )

    return provider.get_tracer(__name__)
