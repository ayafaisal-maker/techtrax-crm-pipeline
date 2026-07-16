select
    _id as lead_note_id,
    tenantId as tenant_id,
    customerProfileId as customer_profile_id,
    content,
    authorId as author_id,
    isArchived as is_archived,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'leadnotes') }}
