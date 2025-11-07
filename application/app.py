import time
import random
import uuid
import json
import logging
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("mock_app")

MALAYSIA_TZ = pytz.timezone('Asia/Kuala_Lumpur')

SERVICES = {
    "payment-service": [
        "Payment processed successfully",
        "Refund issued successfully",
        "Payment verification completed",
        "Payment gateway authorization received",
        "Transaction recorded in ledger",
        "Duplicate payment detected, ignoring request",
        "Chargeback initiated for disputed transaction",
        "Settlement batch triggered for merchant",
        "Payment confirmation sent to user",
        "3D Secure verification completed"
    ],
    "order-service": [
        "Order created successfully",
        "Order updated by user",
        "Order dispatched to courier",
        "Order cancelled by customer",
        "Payment confirmed for order",
        "Order item out of stock, flagged for review",
        "Shipping label generated",
        "Order tracking number assigned",
        "Order status updated to delivered",
        "Invoice generated and emailed"
    ],
    "user-service": [
        "User login successful",
        "User registered successfully",
        "User profile updated",
        "Password reset requested",
        "User session renewed",
        "Email verification completed",
        "Two-factor authentication verified",
        "Failed login attempt detected",
        "User account locked due to repeated failures",
        "User preferences updated"
    ],
    "inventory-service": [
        "Stock updated for product",
        "Inventory sync completed",
        "Low inventory threshold checked",
        "Warehouse stock reconciliation completed",
        "Product restocked successfully",
        "Inventory alert triggered for critical SKU",
        "SKU removed from catalog",
        "Supplier sync started",
        "Supplier sync completed",
        "Inventory adjustment entry created"
    ]
}

ERRORS = [
    ("DB_CONN_TIMEOUT", "Database connection timed out after 30s"),
    ("DB_DEADLOCK", "Deadlock detected during transaction"),
    ("DB_READ_FAIL", "Failed to read record from database"),
    ("DB_WRITE_FAIL", "Failed to write record to database"),
    ("DB_MIGRATION_PENDING", "Table migration in progress, write deferred"),
    ("SERVICE_UNAVAILABLE", "Downstream service unavailable"),
    ("API_500", "Unexpected 500 error from upstream API"),
    ("API_TIMEOUT", "Upstream API did not respond within 10s"),
    ("INVALID_API_RESPONSE", "Malformed response payload from upstream"),
    ("THROTTLED_REQUEST", "Request rate limited by external API"),
    ("DATA_VALIDATION_FAIL", "Invalid data format detected"),
    ("SCHEMA_MISMATCH", "Incoming payload does not match expected schema"),
    ("MISSING_REQUIRED_FIELD", "Required field missing in request body"),
    ("DATA_CONVERSION_ERROR", "Failed to parse numeric field from string"),
    ("NETWORK_RESET", "Connection reset by peer"),
    ("DNS_RESOLUTION_FAIL", "Failed to resolve host name"),
    ("TLS_HANDSHAKE_FAIL", "TLS handshake failed with peer"),
    ("NETWORK_UNREACHABLE", "Network is unreachable"),
    ("BROKEN_PIPE", "Broken pipe while writing to socket"),
    ("QUEUE_BACKPRESSURE", "Message queue under backpressure, retrying"),
    ("QUEUE_TIMEOUT", "Timeout waiting for message acknowledgment"),
    ("CONSUMER_OFFSET_ERROR", "Consumer offset out of range"),
    ("KAFKA_PRODUCE_FAIL", "Failed to publish message to Kafka topic"),
    ("CACHE_MISS", "Cache miss for requested key"),
    ("CACHE_WRITE_FAIL", "Failed to write value to cache store"),
    ("MEMORY_LIMIT_EXCEEDED", "Container memory limit exceeded"),
    ("OOM_KILLED", "Process killed by OOM killer"),
    ("NULL_POINTER", "Unexpected null reference encountered"),
    ("INDEX_OUT_OF_RANGE", "List index out of range"),
    ("TYPE_CAST_ERROR", "Type cast exception occurred"),
    ("UNKNOWN_ERROR", "Unexpected exception caught in main loop"),
    ("FILE_NOT_FOUND", "Configuration file not found on disk"),
    ("DISK_FULL", "Insufficient space on device"),
    ("IO_TIMEOUT", "I/O operation timed out"),
    ("PERMISSION_ERROR", "Permission denied while accessing file"),
    ("METRIC_PUSH_FAIL", "Failed to push metrics to Prometheus gateway"),
    ("LOGGING_BACKEND_UNAVAILABLE", "Logging backend unavailable"),
    ("CONFIG_RELOAD_FAIL", "Failed to reload runtime configuration"),
    ("DEPLOYMENT_ROLLBACK", "Deployment rolled back due to failed health check")
]


def now_myt_iso():
    """Return current timestamp in ISO 8601 format (Malaysia time)."""
    return datetime.now(pytz.utc).astimezone(MALAYSIA_TZ).isoformat()


def generate_log():
    service = random.choice(list(SERVICES.keys()))
    transaction_id = f"txn_{uuid.uuid4().hex[:6]}"
    timestamp = now_myt_iso()

    if random.random() < 0.1:  # 10% error rate
        error_code, description = random.choice(ERRORS)
        log = {
            "timestamp": timestamp,
            "service": service,
            "level": "ERROR",
            "transaction_id": transaction_id,
            "message": f"[{error_code}] {description}"
        }
    else:
        message = random.choice(SERVICES[service])
        log = {
            "timestamp": timestamp,
            "service": service,
            "level": "INFO",
            "transaction_id": transaction_id,
            "message": message,
        }

    logger.info(json.dumps(log))


if __name__ == "__main__":
    for _ in range(random.randint(10, 40)):
        generate_log()
        time.sleep(random.uniform(0.2, 0.8))
