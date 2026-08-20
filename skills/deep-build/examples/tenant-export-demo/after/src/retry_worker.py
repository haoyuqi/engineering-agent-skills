def enqueue_retry(job_id, queue, accepted_job_ids):
    """Enqueue one retry per job ID and report whether it was newly accepted."""
    if job_id in accepted_job_ids:
        return False
    accepted_job_ids.add(job_id)
    queue.append(job_id)
    return True
