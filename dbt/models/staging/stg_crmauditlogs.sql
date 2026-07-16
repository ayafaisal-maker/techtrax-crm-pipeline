select
    _id as audit_log_id,
    tenantId as tenant_id,
    action,
    entityType as entity_type,
    entityId as entity_id,
    entityName as entity_name,
    actor,
    actorName as actor_name,
    actorRole as actor_role,
    timestamp,
    createdAt as created_at
from {{ source('techtrax_raw', 'crmauditlogs') }}
