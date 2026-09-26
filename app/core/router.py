"""
Manual routing engine.
Routes are registered explicitly and matched with Regular Expressions,
so dynamic segments such as /photo/{id} are captured by hand.
"""
import re


class Router:
    """A tiny regex based router that maps (method, path) to a controller action."""

    def __init__(self):
        self.routes = []

    @staticmethod
    def _toRegex(placeholder):
        """Turn {name} into a free group and {name:int} into a digits-only group."""
        name, kind = placeholder.group(1), placeholder.group(2)
        return r"(?P<%s>\d+)" % name if kind == "int" else r"(?P<%s>[^/]+)" % name

    def add(self, method, path, handler):
        """Register a route. '{id:int}' inside the path becomes a named regex group."""
        pattern = re.sub(r"\{([a-zA-Z_]+)(?::(int))?\}", Router._toRegex, path)
        self.routes.append((method.upper(), re.compile("^" + pattern + "$"), handler))

    def dispatch(self, method, path):
        """Find the matching route and call its controller action."""
        pathMatched = False
        for routeMethod, pattern, handler in self.routes:
            match = pattern.match(path)
            if not match:
                continue
            pathMatched = True
            if routeMethod != method.upper():
                continue
            parameters = {key: (int(value) if value.isdigit() else value)
                          for key, value in match.groupdict().items()}
            return handler(**parameters)
        return ("Method Not Allowed", 405) if pathMatched else ("Page Not Found", 404)
