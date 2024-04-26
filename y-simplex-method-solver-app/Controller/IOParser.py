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
    def o_parse_to_arr(input_str: str):
        input_str = input_str.strip()
        return_arr = input_str.split(' ')
        return_arr.insert(0, return_arr[-1])
        return_arr.pop(-1)
        return return_arr
