from Model import FullSolutionStruct, InputStruct, SimplexFile, Singleton
import pathlib


class SaveLoadController(metaclass=Singleton):
    def __init__(self, input_data: InputStruct | None = None, output_data: FullSolutionStruct | None = None):
        self.input_data = input_data
        self.output_data = output_data

    def set_input_data(self, input_data: InputStruct):
        self.input_data = input_data

    def set_output_data(self, output_data: FullSolutionStruct):
        self.output_data = output_data

    def save(self, dirname, simplex_data: SimplexFile):
        temp_path = pathlib.PurePath(dirname)
        filename = temp_path.stem

        simplex_data.filedir = str(temp_path)
        simplex_data.filename = filename

        # Save to a given directory
        json_data = simplex_data.to_json()
        with open(dirname, "w") as file:
            file.write(json_data)
        return simplex_data

    def load(self, file):
        with open(file, "r") as file:
            data = file.read()
            return SimplexFile.from_json(data)
