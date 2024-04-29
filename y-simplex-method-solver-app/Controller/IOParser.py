from Model import ResultStruct


def i_parse_to_str(input_arr: []):
    return_string = ""
    for i in input_arr[:-1]:
        return_string += f"'{i}' "
    return_string += f"'{input_arr[-1]}'"
    return return_string


def i_parse_to_arr(input_arr: []):
    return_arr = []
    for i in input_arr:
        return_arr.append(f"'{i}'")
    return return_arr


def o_parse_results(input_str: str):
    result = ResultStruct("", {}, {})

    if "[" in input_str:
        arr = input_str.split("\n\n")
        result.steps = {a[0]: {b[0]: {c[0]: c[1] for c in enumerate(b[1].split()) if c[1] != "[" and c[1] != "]" and c[1] != " "} for b in enumerate(a[1].splitlines())} for a in enumerate(arr[:-2])}
        result.operations = {a[0]: {b[0]: b[1] for b in enumerate(a[1].split("\n"))} for a in enumerate(arr[-2].strip("{").strip("}").split("}\n{"))}
        result.solution = arr[-1].split()
    else:
        result.solution = input_str.split()
    result.solution.insert(0, result.solution[-1])
    result.solution.pop(-1)
    result.solution = " ".join(result.solution)
    return result
