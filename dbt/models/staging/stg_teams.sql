select
    _id as team_id,
    tenantId as tenant_id,
    name,
    managerId as manager_id,
    teamLeadId as team_lead_id,
    status,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'teams') }}
