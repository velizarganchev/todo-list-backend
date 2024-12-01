from rest_framework.throttling import UserRateThrottle


class TaskThrottle(UserRateThrottle):
    scope = 'task'
