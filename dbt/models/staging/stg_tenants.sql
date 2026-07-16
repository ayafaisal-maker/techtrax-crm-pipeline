select
    _id as tenant_id,
    name,
    email,
    status,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'tenants') }}
