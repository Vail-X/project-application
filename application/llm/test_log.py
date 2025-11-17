import gzip
import json
import requests

log_event_1 = {
    "message": "OperationalError: (psycopg2.OperationalError) connection to server at \"db-prod-cluster.example.com\" failed: timed out (0x0000274c/10060)",
    "level": "ERROR",
    "k8s_container": "data-api-service",
    "k8s_pod": "api-pod-v1-xyz",
    "k8s_namespace": "prod",
    "k8s_app_label": "user-data-service",
    "k8s_job_name": "",
    "k8s_image": "api:v3.5",
    "timestamp": "2025-11-17T11:05:12Z"
}

# 2. Database Deadlock Detected
log_event_2 = {
    "message": "SQLSTATE 40P01: Deadlock found when trying to get lock; try restarting transaction",
    "level": "ERROR",
    "k8s_container": "order-processor",
    "k8s_pod": "processor-15a-4",
    "k8s_namespace": "prod",
    "k8s_app_label": "ecommerce-backend",
    "k8s_job_name": "",
    "k8s_image": "processor:v1.1",
    "timestamp": "2025-11-17T11:08:45Z"
}

# 3. Database Integrity/Constraint Violation
log_event_3 = {
    "message": "IntegrityError: (MySQLdb._exceptions.IntegrityError) (1062, \"Duplicate entry 'user@example.com' for key 'users.email'\")",
    "level": "ERROR",
    "k8s_container": "user-signup-service",
    "k8s_pod": "signup-web-8b-2",
    "k8s_namespace": "prod",
    "k8s_app_label": "user-management",
    "k8s_job_name": "",
    "k8s_image": "web-app:v4.0",
    "timestamp": "2025-11-17T11:10:01Z"
}

# 4. Database Disk Quota Error
log_event_4 = {
    "message": "Error writing to database: disk quota exceeded or storage capacity reached",
    "level": "ERROR",
    "k8s_container": "analytics-worker",
    "k8s_pod": "worker-cron-33",
    "k8s_namespace": "prod",
    "k8s_app_label": "batch-processing",
    "k8s_job_name": "daily-report-job",
    "k8s_image": "worker:v1.2",
    "timestamp": "2025-11-17T11:15:33Z"
}

# Combine all log events into a single list
log_events_list = [log_event_1, log_event_2, log_event_3, log_event_4]

json_data_bytes = json.dumps(log_events_list).encode('utf-8')

compressed_data = gzip.compress(json_data_bytes)

headers = {
    'Content-Encoding': 'gzip',
    'Content-Type': 'application/json' 
}

# The data parameter is now ONLY the compressed binary payload
response = requests.post(
    "http://localhost:8081/analyze",
    data=compressed_data,
    headers=headers # Pass the explicit headers
)

print(response.json())