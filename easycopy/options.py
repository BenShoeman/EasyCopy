from collections import defaultdict
import json
import re

DEFAULTS = {
    "min_year": 1600
}

# json_str isn't explicitly a JSON string, also can have Javascript-like regex
# syntax /REGEX/
def get_options(json_str):
    if json_str is None:
        # This means inputted json_str wasn't regex matched, so no options
        return defaultdict(lambda: None, DEFAULTS)
    
    # Replace javascript-like regex literals with strings JSON can use
    json_str = re.sub(r'/((?:\\/|[^/])*)/', '"\\1"', json_str).replace("\\", "\\\\")
    try:
        opts = defaultdict(lambda: None, json.loads(json_str))
    except json.decoder.JSONDecodeError:
        # If JSON improperly formatted, just use defaults
        opts = defaultdict(lambda: None, DEFAULTS)

    # Then get options
    if opts["min_year"] is None:
        opts["min_year"] = DEFAULTS["min_year"]
    if opts["regexsub"] is not None and len(opts["regexsub"]) > 1:
        opts["user_regex"] = re.compile(opts["regexsub"][0])
        opts["user_subst"] = opts["regexsub"][1]
        del opts["regexsub"]
    if opts["prepend"] is None:
        opts["prepend"] = ""
    
    return opts