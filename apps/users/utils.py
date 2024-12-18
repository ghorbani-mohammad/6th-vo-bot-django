from django.core.cache import cache


def user_filter(request):
    filter_string = {}
    filter_mappings = {"search": "username__icontains"}
    for key in request.GET:
        if request.GET.get(key) and key != "page":
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string


def clear_horoscope_cache():
    keys = cache.keys("horoscope_*")  # Fetch all keys matching the pattern

    for key in keys:
        cache.delete(key)


def clear_suggestion_cache():
    keys = cache.keys("profile_suggestions_*")  # Fetch all keys matching the pattern

    for key in keys:
        cache.delete(key)
