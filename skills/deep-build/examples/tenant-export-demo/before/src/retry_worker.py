def enqueue_retry(job_id, queue):
    """Unsafe starting point: repeated requests enqueue duplicates."""
    queue.append(job_id)
    return True
