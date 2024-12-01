from rest_framework.throttling import UserRateThrottle


class TaskThrottle(UserRateThrottle):
    scope = 'task'

    def allow_request(self, request, view):

        new_scope = 'task-' + request.method.lower()  # task-post, task-put, task-delete
        if new_scope in self.THROTTLE_RATES:
            self.scope = new_scope
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)
