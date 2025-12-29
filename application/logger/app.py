import time
import random
import uuid
import json
from datetime import datetime
import pytz

# Configuration
MALAYSIA_TZ = pytz.timezone("Asia/Kuala_Lumpur")

BANKS = [
    "Maybank",
    "CIMB",
    "RHB",
    "Public Bank",
    "Hong Leong",
    "GrabPay",
    "TNG eWallet",
    "ShopeePay",
]
LOCATIONS = [
    "Cheras",
    "Damansara",
    "Puchong",
    "Bangsar",
    "Subang Jaya",
    "Penang",
    "Johor Bahru",
    "Ipoh",
]
AUTH_METHODS = ["OIDC", "SAML 2.0", "Biometric", "SMS-OTP", "Email-Link", "JWT-Bearer"]
DEVICES = [
    "iPhone 15 Pro",
    "Samsung S23",
    "MacBook Air (M2)",
    "Chrome/Windows 11",
    "Firefox/Linux",
]
COURIERS = ["NinjaVan", "J&T Express", "PosLaju", "Lalamove", "DHL eCommerce"]


def get_message(service, level):
    if service == "identity-provider":
        if level == "INFO":
            return random.choice(
                [
                    f"User session initiated via {random.choice(AUTH_METHODS)} login flow",
                    f"MFA challenge successfully bypassed by trusted device: {random.choice(DEVICES)}",
                    f"Password policy update: Forced rotation scheduled for {random.randint(200, 500)} accounts in {random.choice(LOCATIONS)}",
                    f"Account recovery link sent to registered mobile ending in ***{random.randint(100, 999)}",
                    "Administrative role 'AUDITOR' assigned to system-user-id: "
                    + uuid.uuid4().hex[:6],
                    "JWT signing key rotated successfully using RS256 algorithm",
                    f"User login from {random.choice(LOCATIONS)} verified with high confidence score",
                    f"New device fingerprint registered: {uuid.uuid4().hex[:12]}",
                    f"SSO assertion validated for tenant-{random.randint(10,99)} using {random.choice(AUTH_METHODS)}",
                    f"Idle session timeout extended by policy engine for user context {uuid.uuid4().hex[:8]}",
                    "Risk-based authentication evaluated: no additional challenge required",
                    f"Consent record updated for data-scope 'profile:read' at {random.choice(LOCATIONS)} region",
                    "Background job completed: user-claims cache warmed successfully",
                    f"Account status transitioned from PENDING to ACTIVE for user-{random.randint(1000,9999)}",
                ]
            )
        else:
            return random.choice(
                [
                    f"[BRUTE_FORCE] {random.randint(10, 50)} failed login attempts detected for IP 202.184.{random.randint(0,255)}.{random.randint(0,255)}",
                    f"[TOKEN_EXPIRED] Refresh token for session {uuid.uuid4().hex[:8]} revoked due to security policy",
                    f"[OIDC_DISCOVERY_FAIL] Unable to fetch metadata from {random.choice(['Google', 'Azure AD', 'Okta'])} endpoint",
                    "[SECURITY_VIOLATION] Anonymous user attempted to access restricted /admin/config resource",
                    f"[MFA_TIMEOUT] User failed to complete MFA challenge within {random.randint(30,90)} seconds",
                    f"[INVALID_SIGNATURE] JWT validation failed: signature mismatch for key-id {uuid.uuid4().hex[:6]}",
                    "[ACCOUNT_LOCKED] User account locked after exceeding maximum authentication retries",
                    f"[SESSION_REVOKED] Active sessions terminated due to policy update for tenant-{random.randint(1,20)}",
                    "[IDP_BACKEND_ERROR] Identity datastore returned 500 during credential lookup",
                ]
            )
    elif service == "notification-service":
        if level == "INFO":
            return random.choice(
                [
                    f"OTP message dispatched via SMS gateway to masked number ***{random.randint(1000,9999)}",
                    f"Email notification queued for delivery: template=PAYMENT_SUCCESS, locale=en_MY",
                    f"Push notification delivered successfully to device token {uuid.uuid4().hex[:10]}",
                    f"Webhook notification sent to merchant endpoint for event PAYMENT_COMPLETED",
                    f"Bulk notification campaign started for {random.randint(100,1000)} recipients",
                    f"Delivery status updated: message-id {uuid.uuid4().hex[:8]} marked as DELIVERED",
                    f"Notification template cache refreshed for version v{random.randint(1,5)}.{random.randint(0,9)}",
                    "Retry worker completed backlog processing with zero failures",
                    f"SMS provider switched to secondary route due to latency optimization",
                    f"Notification throttling rules evaluated: no limits exceeded",
                    f"Message personalization applied using dynamic attributes",
                    f"Event-driven notification published for ORDER_SHIPPED",
                ]
            )
        else:
            return random.choice(
                [
                    "[SMS_GATEWAY_TIMEOUT] Primary SMS provider did not respond within SLA",
                    "[EMAIL_BOUNCE] Permanent failure returned by upstream SMTP relay",
                    f"[PUSH_TOKEN_INVALID] Device token {uuid.uuid4().hex[:10]} rejected by provider",
                    "[WEBHOOK_FAILED] Merchant endpoint returned HTTP 500",
                    "[RATE_LIMIT_EXCEEDED] Notification throughput exceeded configured limits",
                    f"[DELIVERY_RETRY_EXHAUSTED] Message-id {uuid.uuid4().hex[:8]} failed after max retries",
                    "[TEMPLATE_RENDER_ERROR] Missing required placeholder in notification template",
                    "[PROVIDER_OUTAGE] All active notification routes are unavailable",
                    "[QUEUE_BACKLOG] Notification queue depth exceeded warning threshold",
                    "[PAYLOAD_TOO_LARGE] Notification payload rejected by downstream service",
                ]
            )
    elif service == "payment-gateway":
        if level == "INFO":
            return random.choice(
                [
                    f"Transaction authorized: {random.uniform(5.0, 2000.0):.2f} MYR via {random.choice(BANKS)}",
                    f"Settlement file 'FINEXUS_SETTLE_{random.randint(100, 999)}.dat' transmitted to {random.choice(BANKS)} SFTP",
                    f"Callback received from {random.choice(BANKS)}: Payment for TXN-{uuid.uuid4().hex[:6].upper()} confirmed",
                    f"Merchant payout for branch in {random.choice(LOCATIONS)} cleared for {random.uniform(1000, 5000):.2f} MYR",
                    f"Currency exchange rate updated: 1 USD = {random.uniform(4.6, 4.8):.4f} MYR",
                    "3D Secure 2.0 verification completed for high-value transaction",
                    f"New merchant onboarding: 'Retail_Partner_{random.randint(100,999)}' approved for direct debit",
                    f"Fraud scoring completed: risk score {random.randint(1,20)} assigned to transaction",
                    f"Batch reconciliation job completed for business date {datetime.now().date()}",
                    f"Partial capture processed for split payment TXN-{uuid.uuid4().hex[:6].upper()}",
                    "Payment routing optimized based on issuer availability metrics",
                    f"Refund successfully issued for original transaction TXN-{random.randint(10000,99999)}",
                ]
            )
        else:
            return random.choice(
                [
                    f"[GATEWAY_TIMEOUT] {random.choice(BANKS)} API did not respond within the 10000ms SLA",
                    f"[AUTH_REJECT] {random.choice(BANKS)} returned error code 05: Do not honor transaction",
                    f"[INTEGRITY_FAIL] MAC mismatch for inbound notification from {random.choice(BANKS)} gateway",
                    f"[SSL_EXPIRED] Communication failed: Upstream SSL certificate for {random.choice(BANKS)} has expired",
                    "[DUPLICATE_TXN] Duplicate transaction reference detected during authorization phase",
                    f"[RATE_LIMITED] Throttled by {random.choice(BANKS)} due to excessive request volume",
                    "[SETTLEMENT_MISMATCH] Net settlement amount does not balance with transaction ledger",
                    f"[CALLBACK_INVALID] Signature verification failed for callback from {random.choice(BANKS)}",
                    "[FX_PROVIDER_ERROR] Unable to retrieve real-time FX rates from upstream provider",
                ]
            )

    elif service == "warehouse-logistics-v2":
        if level == "INFO":
            return random.choice(
                [
                    f"Shipment dispatched: Order ORD-{random.randint(1000, 9999)} assigned to {random.choice(COURIERS)}",
                    f"Inbound stock arrival: {random.randint(50, 200)} units of Electronics received at {random.choice(LOCATIONS)} hub",
                    f"Inventory reconciliation: Physical count matches system records for zone {random.choice(['A', 'B', 'C'])}-{random.randint(1, 10)}",
                    f"Barcode scanner #{random.randint(1, 5)} firmware updated to v4.2.0 successfully",
                    f"Transfer request: Moving {random.randint(10, 50)} units from {random.choice(LOCATIONS)} to {random.choice(LOCATIONS)}",
                    "Warehouse environment sensors reporting normal temperature/humidity",
                    f"Manifest for courier pickup finalized with {random.randint(10, 100)} line items",
                    f"Pick-and-pack operation completed for wave-{random.randint(100,999)}",
                    f"Dock scheduling optimized for next delivery window at {random.choice(LOCATIONS)}",
                    f"Cycle count completed with variance below acceptable threshold",
                    "Automated sorter operating within normal throughput range",
                    f"Return merchandise authorization (RMA) created for order ORD-{random.randint(1000,9999)}",
                ]
            )
        else:
            return random.choice(
                [
                    "[DB_LOCK_TIMEOUT] Lock wait timeout exceeded while updating stock availability table",
                    f"[COURIER_API_ERROR] {random.choice(COURIERS)} returned 503 Service Unavailable for label generation",
                    f"[LOST_STOCK] Negative inventory detected for SKU-{random.randint(100, 999)} at {random.choice(LOCATIONS)} warehouse",
                    f"[PARSE_ERROR] Failed to ingest 'manifest_{random.randint(1,5)}.csv': Column mismatch at row {random.randint(1, 100)}",
                    "[PICK_FAILURE] Item could not be located during picking operation",
                    f"[MISROUTE] Shipment assigned to incorrect hub: expected {random.choice(LOCATIONS)}",
                    "[SENSOR_ALERT] Temperature exceeded safe threshold in cold storage zone",
                    f"[WEIGHT_MISMATCH] Declared parcel weight differs from measured value",
                    "[INVENTORY_DRIFT] Repeated reconciliation discrepancies detected for high-volume SKU",
                ]
            )


def generate_log():
    service = random.choice(
        [
            "identity-provider",
            "payment-gateway",
            "warehouse-logistics-v2",
            "notification-service",
        ]
    )

    # 1% Error Rate
    level = random.choices(["INFO", "ERROR"], weights=[97, 3])[0]

    log_entry = {
        "timestamp": datetime.now(MALAYSIA_TZ).isoformat(),
        "service": service,
        "level": level,
        "trace_id": str(uuid.uuid4()),
        "message": get_message(service, level),
    }

    print(json.dumps(log_entry))


if __name__ == "__main__":
    for _ in range(random.randint(10, 20)):
        generate_log()
        time.sleep(random.uniform(0.2, 0.8))
