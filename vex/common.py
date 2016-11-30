from datetime import *

from django.utils.termcolors import colorize


def log(msg, color="green"):
    print(colorize("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] " + msg, fg=color))


def dict_search(d, k, v):
    for i in range(0, len(d)):
        if d[i][k] == v:
            return i
    return None


def tuple_search(t, k, v):
    for e in t:
        if e[k] == v:
            return e
    return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


if __name__ == "__main__":
    log("Common library is ready to use.")
