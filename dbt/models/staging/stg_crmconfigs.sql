select
    _id as crm_config_id,
    tenantId as tenant_id,
    maxFollowUpAttempts as max_follow_up_attempts,
    maxSnoozeDurationDays as max_snooze_duration_days,
    unreachableHoldPeriodHours as unreachable_hold_period_hours,
    isPipelineActive as is_pipeline_active,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'crmconfigs') }}
