select
    _id as lead_history_id,
    tenantId as tenant_id,
    customerProfileId as customer_profile_id,
    fromStageId as from_stage_id,
    toStageId as to_stage_id,
    actor,
    actorId as actor_id,
    enteredAt as entered_at,
    exitedAt as exited_at,
    durationMinutes as duration_minutes,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'leadhistories') }}
