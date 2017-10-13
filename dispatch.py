from collections import defaultdict
from functools import wraps
import inspect


dispatches = defaultdict(lambda: [])


def argspec_matches(argspec, args, kwargs):
    for i, arg in enumerate(args):
        if not isinstance(arg, argspec.annotations[argspec.args[i]]):
            return False

    return True


def dispatch_me(function):
    global dispatches

    argspec = inspect.getfullargspec(function)
    dispatches[function.__name__].append((argspec, function))

    @wraps(function)
    def wrapper(*args, **kwargs):
        for argspec, f in dispatches[function.__name__]:
            if argspec_matches(argspec, args, kwargs):
                return f(*args, **kwargs)

        raise ValueError('No version found for those arguments!')

    return wrapper


@dispatch_me
def do_it(x: int):
    print('Je suis an int')


@dispatch_me
def do_it(x: float):
    print('Je suis a float')


do_it(10)
do_it(10.5)
