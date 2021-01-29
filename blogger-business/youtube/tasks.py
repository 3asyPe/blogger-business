from celery import shared_task

from .models import Youtube


@shared_task
def update_all_channel_statistics_task(*args, **kwargs):
    youtubes = Youtube.objects.get_active_accounts()
    for youtube in youtubes:
        youtube.statistics.update_statistics_for_last_month()
        youtube.statistics.update_total_statistics()
