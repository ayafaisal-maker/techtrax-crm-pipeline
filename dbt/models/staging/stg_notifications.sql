select
    _id as notification_id,
    tenantId as tenant_id,
    receiverId as receiver_id,
    senderId as sender_id,
    type,
    title,
    module,
    urgency,
    isRead as is_read,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'notifications') }}
