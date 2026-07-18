select
    _id as leave_type_id,
    tenantId as tenant_id,
    slug,
    name,
    description,
    isPaid as is_paid,
    isActive as is_active,
    isSoftDeleted as is_soft_deleted,
    isSystemReserved as is_system_reserved,
    balance,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'crmleavetypes') }}
