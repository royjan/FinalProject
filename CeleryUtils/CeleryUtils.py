def create_chords(jobs, callback_function, **kwargs):
    from celery import chord
    result = chord(jobs, callback_function.s(**kwargs))
    return result


def group_tasks(celery_task, payload, dataset_name):
    group = [celery_task.s(config=_p, dataset_name=dataset_name) for _p in payload]
    return group
