select
    _id as stage_id,
    tenantId as tenant_id,
    name,
    slug,
    sortOrder as sort_order,
    stageType as stage_type,
    slaHours as sla_hours,
    status,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'stages') }}
