select
    _id as shift_template_id,
    tenantId as tenant_id,
    name,
    description,
    isSystemTemplate as is_system_template,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'crmshifttemplates') }}
