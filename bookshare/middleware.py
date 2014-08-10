from django.shortcuts import render

class AssertionErrorMiddleware(object):
    def process_exception(self, request, exception):
	if isinstance(exception, AssertionError):
            context = dict(
                message = str(exception),
            )
            return render(request, 'error.html', context)
        return None
