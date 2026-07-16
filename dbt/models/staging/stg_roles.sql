select
    _id as role_id,
    tenantId as tenant_id,
    title,
    slug,
    type,
    module,
    permissionTier as permission_tier,
    teamId as team_id,
    status,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'roles') }}
