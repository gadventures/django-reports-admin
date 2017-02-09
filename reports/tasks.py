from celery.task import task


@task()
def report_task(report_class, user_id, query, app_label, model_name):
    '''
    Instantiates the report class, runs the report, and notifies
    the user.
    '''
    report = report_class(
        user_id=user_id,
        query=query,
        app_label=app_label,
        model_name=model_name
    )
    report.run_report()
