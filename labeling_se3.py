from parsing import parse_measurement

def evaluate_dc50(measurement, threshold):
    measurement_type = measurement["type"]

    if measurement_type in {"missing", "unparsed", "multiple"}: 
        return "ambiguous"

    lower = measurement.get("lower")
    upper = measurement.get("upper")

    if lower is not None and lower > threshold:
        return "fail"
    if upper is not None and upper <= threshold:
        return "pass"

    return "ambiguous"

def evaluate_dmax(measurement, threshold):
    measurement_type = measurement["type"]

    if measurement_type in {"missing", "unparsed", "multiple"}: 
        return "ambiguous"

    lower = measurement.get("lower")
    upper = measurement.get("upper")

    if upper is not None and upper < threshold:
        return "fail"
    if lower is not None and lower >= threshold:
        return "pass"

    return "ambiguous"

def label_se3(dc50_status, dmax_status):
    if dc50_status == "pass" and dmax_status == "pass":
        return "positive"

    if dc50_status == "fail" or dmax_status == "fail":
        return "negative"

    return "ambiguous"

# #tests
# print("DC50 tests")
# print("20:", evaluate_dc50(parse_measurement("20"), 100))
# print("<5:", evaluate_dc50(parse_measurement("<5"), 100))
# print(">1000:", evaluate_dc50(parse_measurement(">1000"), 100))
# print("50-500:", evaluate_dc50(parse_measurement("50-500"), 100))

# print("\nDmax tests")
# print("95:", evaluate_dmax(parse_measurement("95"), 80))
# print(">95:", evaluate_dmax(parse_measurement(">95"), 80))
# print("<50:", evaluate_dmax(parse_measurement("<50"), 80))
# print("50-90:", evaluate_dmax(parse_measurement("50-90"), 80))