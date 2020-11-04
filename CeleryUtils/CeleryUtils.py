def create_chords(jobs, callback_function, **kwargs):
    from celery import chord
    result = chord(jobs, callback_function.s(**kwargs))
    return result


def group_tasks(params, celery_task, **kwargs):
    group = [celery_task.s(param, **kwargs) for param in params]
    return group
