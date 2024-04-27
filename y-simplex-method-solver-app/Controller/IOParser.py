from Model import ResultStruct


class IOParser:
    @staticmethod
    def i_parse_to_str(input_arr: []):
        return_string = ""
        for i in input_arr[:-1]:
            return_string += f"'{i}' "
        return_string += f"'{input_arr[-1]}'"
        return return_string

    @staticmethod
    def i_parse_to_arr(input_arr: []):
        return_arr = []
        for i in input_arr:
            return_arr.append(f"'{i}'")
        return return_arr

    @staticmethod
    def o_parse_results(input_str: str):
        result = ResultStruct([], [])
        if "[" in input_str:
            arr = input_str.split("\n\n")
            result.steps = [[[c for c in b.split() if c != "[" and c != "]" and c != " "] for b in a.splitlines()] for a in arr[:-1]]
            result.solution = arr[-1].split()
        else:
            result.solution = input_str.split()
        result.solution.insert(0, result.solution[-1])
        result.solution.pop(-1)
        return result
