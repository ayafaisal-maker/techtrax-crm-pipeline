select
    _id as customer_profile_id,
    tenantId as tenant_id,
    firstName as first_name,
    lastName as last_name,
    email,
    phone,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at,
    PARSE_JSON(customFields) as custom_fields
from {{ source('techtrax_raw', 'customerprofiles') }}