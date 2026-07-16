select
    _id as sync_log_id,
    tenantId as tenant_id,
    configId as config_id,
    status,
    rowsProcessed as rows_processed,
    leadsCreated as leads_created,
    rowsFailed as rows_failed,
    syncStartedAt as sync_started_at,
    syncCompletedAt as sync_completed_at,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'googlesheetssynclogs') }}
