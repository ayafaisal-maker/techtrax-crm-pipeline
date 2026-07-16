select
    _id as file_asset_id,
    tenantId as tenant_id,
    fileName as file_name,
    originalName as original_name,
    contentType as content_type,
    size,
    status,
    ownerId as owner_id,
    uploadedBy as uploaded_by,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'fileassets') }}
