select
    _id as shift_id,
    tenantId as tenant_id,
    userId as user_id,
    shiftTemplateId as shift_template_id,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'crmshifts') }}
