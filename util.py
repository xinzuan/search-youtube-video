from typing import List, Union
def isNaN(num: str):
    try:
        int(num)
        return False
    except:
        return True

def buildTraceback(e: Exception):
    trace =[]
    tb = e.__traceback__

    while tb is not None:
        trace.append({
            "filename": tb.tb_frame.f_code.co_filename,
            "name": tb.tb_frame.f_code.co_name,
            "line_no": tb.tb_lineno,
        })
        tb = tb.tb_next
    
    return str({
        "type": type(e).__name__,
        "message": str(e),
        "trace": trace,
    })

def getValue(source: dict, path: List[str]) -> Union[str, int, dict, None]:
    value = source
    for key in path:
        if type(key) is str:
            if key in value.keys():
                value = value[key]
            else:
                value = None
                break
        elif type(key) is int:
            if len(value) != 0:
                value = value[key]
            else:
                value = None
                break
    return value
