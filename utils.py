from typing import List, Dict, Any

def kvlist2dict(kvlist: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = {}
    for kv in kvlist:
        result[kv['k']] = kv['v']
    return result