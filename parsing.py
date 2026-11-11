import pandas as pd

def parse_measurement(value):
    raw = value

    #missing value
    if pd.isna(value):
        return {"type": "missing", "raw": raw, "lower": None, "upper": None}

    value = str(value).strip()
    value = (value.replace(",", "").replace("＞", ">").replace("＜", "<"))

    #missing value (nd)
    if value.lower() in ["nd", "n.d.", "n.d", "nd.", "n.d,", "not determined", "na"]:
        return {"type": "missing", "raw": raw, "lower": None, "upper": None}

    #multiple measurements (corresponding to same row/compound)
    if "/" in value:
        values = [parse_measurement(x.strip()) for x in value.split("/")]
        return {"type": "multiple", "raw": raw, "values": values}

    #conditional ranges
    if "and" in value:
        lower_part, upper_part = value.split("and")
        lower = float(lower_part.replace(">", "").replace("=","").strip())
        upper = float(upper_part.replace("<", "").replace("=","").strip())
        return {"type": "range", "raw": raw, "lower": lower, "upper": upper}

    #upper bounds (double symbol)
    if value.startswith("<="):
        number = float(value[2:])
        return {"type": "upper_bound", "raw": raw, "lower": None, "upper": number}
    
    #lower bounds (double symbol)
    if value.startswith(">="):
        number = float(value[2:])
        return {"type": "lower_bound", "raw": raw, "lower": number, "upper": None}
    
    #upper bounds (single symbol)
    if value.startswith("<"):
        number = float(value[1:])
        return {"type": "upper_bound", "raw": raw, "lower": None, "upper": number}

    #lower bounds (single symbol)
    if value.startswith(">"):
        number = float(value[1:])
        return {"type": "lower_bound", "raw": raw, "lower": number, "upper": None}

    #range ~
    if "~" in value:
        lower, upper = value.split("~")
        return {"type": "range", "raw": raw, "lower": float(lower), "upper": float(upper)}

    #range -
    if value.count("-") == 1: #found dates in dmax values (have multiple "-"), so only parse if there is exactly one "-"
        try:
            lower, upper = value.split("-")
            return {"type": "range", "raw": raw, "lower": float(lower), "upper": float(upper)}
        except ValueError:
            return {"type": "unparsed", "raw": raw, "lower": None, "upper": None}

    #exact values
    try: 
        number = float(value)
        return {"type": "exact", "raw": raw, "lower": number, "upper": number}
    except ValueError:
        return {"type": "unparsed", "raw": raw, "lower": None, "upper": None}

# print(parse_measurement("N.D."))
# print(parse_measurement("5"))
# print(parse_measurement("<5"))
# print(parse_measurement(">5"))
# print(parse_measurement("<=100"))
# print(parse_measurement(">=95"))
# print(parse_measurement("10~100"))
# print(parse_measurement("50-500"))
# print(parse_measurement(">5 and <50"))
# print(parse_measurement(">30,000"))
# print(parse_measurement("> 10000"))
# print(parse_measurement("＞1000"))
# print(parse_measurement("N.D."))
# print(parse_measurement("ND."))
# print(parse_measurement("nd"))
# print(parse_measurement("N.D,"))
# print(parse_measurement("87/66"))