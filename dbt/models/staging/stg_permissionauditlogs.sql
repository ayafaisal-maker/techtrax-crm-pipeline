select
    _id as permission_audit_log_id,
    tenantId as tenant_id,
    action,
    performedBy as performed_by,
    targetUser as target_user,
    targetRole as target_role,
    previousRoleId as previous_role_id,
    newRoleId as new_role_id,
    timestamp,
    createdAt as created_at
from {{ source('techtrax_raw', 'permissionauditlogs') }}
