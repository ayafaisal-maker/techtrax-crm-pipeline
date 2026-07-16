select
    _id as clock_record_id,
    tenantId as tenant_id,
    userId as user_id,
    day,
    clockIn as clock_in,
    clockOut as clock_out,
    status,
    shiftMinutes as shift_minutes,
    workedMinutes as worked_minutes,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'crmclockrecords') }}
