class Args:
    @classmethod
    def parse(cls, fields: list, args: tuple, kwargs: dict) -> tuple:
        # Parse fixed args
        results = []
        for i, field in enumerate(fields):
            if i < len(args):
                results.append(args[i])
            else:
                value = kwargs.get(field, None)
                if value:
                    results.append(value)
                    # Args comes from kwargs, pop the key
                    kwargs.pop(field)
        results.append(kwargs)
        return tuple(results)
