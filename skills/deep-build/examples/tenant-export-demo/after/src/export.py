def export_rows(rows, requested_tenant):
    """Return only rows owned by the requested tenant."""
    return [row for row in rows if row["tenant_id"] == requested_tenant]
