from ceci import PipelineStage
from descformats import TextFile, FitsFile, HDFFile, YamlFile

# This class represents one step in the pipeline
class sample_pipeline_collectionStage1(PipelineStage):
    name = "sample_pipeline_collectionStage1"
    #
    inputs = [
        ('some_input_tag', TextFile),
    ]
    outputs = [
        ('some_output_tag', TextFile),
        # More inputs can go here
    ]
    config_options = {
        'price_of_fish': float,  # This parameter is required in the test/config.yaml file
        'number_of_roads': 42,   # This parameter will take the default value 42 if not specified
        }

    def run(self):

        fish = self.config['price_of_fish']
        roads = self.config['number_of_roads']

        input_file = self.open_input('some_input_tag')
        input_data = input_file.read()
        input_file.close()

        # You would normally call some other function or method
        # here to generate some output.  You can use self.comm, 
        # self.rank, and self.size to use MPI.

        output = f"""
Original input text was:
{input_data}

How many roads must a man walk down?  {roads}
Price of {fish}
        """

        output_file = self.open_output('some_output_tag')
        output_file.write(output)
        output_file.close()
