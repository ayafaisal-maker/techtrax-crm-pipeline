select
    _id as custom_field_id,
    tenantId as tenant_id,
    fieldName as field_name,
    fieldType as field_type,
    label,
    location,
    module,
    isMandatory as is_mandatory,
    isActive as is_active,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'customfields') }}
