select
    _id as audit_log_id,
    tenantId as tenant_id,
    action,
    entity,
    method,
    statusCode as status_code,
    timestamp,
    createdAt as created_at
from {{ source('techtrax_raw', 'auditlogs') }}
