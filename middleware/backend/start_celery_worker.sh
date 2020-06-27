#!/bin/sh
exec celery worker --app crawler -l info -c 1 -E --queues queue_crawler