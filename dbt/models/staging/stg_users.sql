select
    _id as user_id,
    tenantId as tenant_id,
    firstName as first_name,
    lastName as last_name,
    email,
    phone,
    status,
    role,
    roleId as role_id,
    teamId as team_id,
    permissionTier as permission_tier,
    isOnline as is_online,
    isClockedIn as is_clocked_in,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'users') }}
qualify row_number() over (partition by _id order by updatedAt desc) = 1
