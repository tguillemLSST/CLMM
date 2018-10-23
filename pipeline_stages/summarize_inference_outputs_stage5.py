from ceci import PipelineStage
from descformats import TextFile, FitsFile, HDFFile, YamlFile

class SummarizeInferenceOutputsStage5(PipelineStage):
    '''Fifth stage of the pipeline where we summarize the results of
importance sampled chains per cluster collection.

    The inputs are importance sampled outputs per collection, and the
    outputs are the summary statistic(s). e.g. most likely mass with
    errorbars, concentration, noise levels, etc.

    The pipeline loops through the collections' outputs, and
    summarizes.

    It can do this in parallel if needed.  We might want to move some
    of the functionality here (e.g. the I/O) into a general parent
    class.

    '''

    name = "summarize_inference_outputs_stage5"

    inputs = [
        ('importance_sampling_results', HDFFile), # Leaving this as an
                                            # HDFFile we can perhaps
                                            # concatenate the data
                                            # into as a preprocessing
                                            # step external to the
                                            # pipeline.
    ]

    outputs = [
        ('summarized_inference_outputs', HDFFile), 
    ] # ehh... not sure how we'll want to store objects, but leaving
      # this as an HDFFile that we can un-concatenate if needed.

    config_options = {
        'galaxy_cluster_data_dir': str,  # This parameter is required in the test/config.yaml file
        'galaxy_cluster_file_type': str, # This parameter is required in the test/config.yaml file
        }

    def run(self):
        '''
        This summarizes importance sampling outputs per collection (e.g. bins) of clusters
        
        - Prepares the output HDF5 File
        - Loads in the collections' importance sampled outputs
        - Summarizes the importance sampling result
        - Writes the summarized information to output
        - Closes the output file

        '''

        gc_datadir = self.config['galaxy_cluster_data_dir']
        gc_filetype = self.config['galaxy_cluster_file_type']

        input_file = self.open_input('importance_sampling_outputs')

        # Check how many objects we are running on
        ncollections = self.config['num_collections']

        input_data = input_file.read()
        input_file.close()

        # Prepare the output file
        output_file = self.prepare_output(ncollections)

        # You would normally call some other function or method
        # here to generate some output.  You can use self.comm, 
        # self.rank, and self.size to use MPI.

        # IO tool options:
        # self.iterate_fits(tag, hdunum, cols, chunk_rows)
        # self.iterate_hdf(tag, group_name, cols, chunk_rows)

        chunk_rows = self.config['chunk_rows']

        # Loop through chunks of data, can use MPI here.
        for start, end, data in self.iterate_hdf(tag, group_name, cols, chunk_rows) :
            print(f"Process {self.rank} summarizing each importance sampled output for rows {start}-{end}")

            # Summarize
            summarized_inference_data = self.summarize_inference_output(data)

            # Save this chunk of data to the output file
            self.write_output(output_file, start, end, summarized_inference_data)
        

        # Synchronize processors
        if self.is_mpi():
            self.comm.Barrier()

        # Finish
        output_file.close()

    def summarize_inference_output(self, data) :
        '''
        Take in results of importance sampling and summarize
        '''

        pass

