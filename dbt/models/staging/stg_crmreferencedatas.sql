select
    _id as reference_data_id,
    tenantId as tenant_id,
    category,
    name,
    code,
    isDefault as is_default,
    isActive as is_active,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'crmreferencedatas') }}
