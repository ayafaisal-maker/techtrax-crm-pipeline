select
    _id as google_sheets_config_id,
    tenantId as tenant_id,
    teamId as team_id,
    name,
    spreadsheetId as spreadsheet_id,
    isRoundRobin as is_round_robin,
    isActive as is_active,
    lastSyncAt as last_sync_at,
    lastSyncStatus as last_sync_status,
    totalLeadsCreated as total_leads_created,
    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'googlesheetsconfigs') }}
