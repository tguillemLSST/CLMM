from ceci import PipelineStage
from descformats import TextFile, FitsFile, HDFFile, YamlFile

class RunChainPerGCStage2(PipelineStage):
    '''Second stage of the CLMM pipeline where we use the inferrer to sample
likelihood of parameters on each cluster object.

    The inputs are the populated galaxy cluster objects, the outputs
    are the chains.

    The pipeline loops through input galaxy cluster objects, using the
    inference manager to collect relevant data for the Inferrer object. 

    It can do this in parallel if needed.  We might want to move some
    of the functionality here (e.g. the I/O) into a general parent
    class.

    '''

    name = "run_chain_per_gc_stage2"

    inputs = [
        ('populated_galaxy_cluster_objects', HDFFile), # Leaving this as an
                                            # HDFFile we can perhaps
                                            # concatenate the data
                                            # into as a preprocessing
                                            # step external to the
                                            # pipeline.
    ]

    outputs = [
        ('galaxy_cluster_objects_with_chains', HDFFile), 
    ] # ehh... not sure how we'll want to store objects, but leaving
      # this as an HDFFile that we can un-concatenate if needed.

    config_options = {
        'galaxy_cluster_data_dir': str,  # This parameter is required in the test/config.yaml file
        'galaxy_cluster_file_type': str, # This parameter is required in the test/config.yaml file
        'subsample_rate': 1,   # This parameter will take the default value 1 if not specified
        }

    def get_num_clusters(self, input_file) :
        ''' Quick method to return number of galaxy clusters we are running on.'''
        pass

    def run(self):
        '''
        This should *just* deal with the loading of data and populating the galaxy cluster objects.
        
        - Prepares the output HDF5 File
        - Loads in the galaxy cluster objects
        - Runs chains per galaxy cluster object
        - Populates GalaxyCluster objects with the chain information
        - Writes the output GalaxyCluster objects to output
        - Closes the output file

        '''

        gc_datadir = self.config['galaxy_cluster_data_dir']
        gc_filetype = self.config['galaxy_cluster_file_type']

        input_file = self.open_input('populated_galaxy_clusters')

        # Check how many objects we are running on
        nclusters = self.get_num_clusters(input_file)

        input_data = input_file.read()
        input_file.close()

        # Prepare the output file
        output_file = self.prepare_output(nclusters)

        # You would normally call some other function or method
        # here to generate some output.  You can use self.comm, 
        # self.rank, and self.size to use MPI.

        # IO tool options:
        # self.iterate_fits(tag, hdunum, cols, chunk_rows)
        # self.iterate_hdf(tag, group_name, cols, chunk_rows)

        chunk_rows = self.config['chunk_rows']
        # Loop through chunks of data, can use MPI here.
        for start, end, data in self.iterate_hdf(tag, group_name, cols, chunk_rows) :
            print(f"Process {self.rank} running chains on galaxy cluster objects for rows {start}-{end}")

            # Use manager to collect inferrer relevant data from galaxy cluster objects
            inferrer_input = self.prepare_gc_data(data)

            # Make inference per cluster
            inferrer_output_chains = self.make_inference(inferrer_input)

            # Save this chunk of data to the output file
            self.write_output(output_file, start, end, inferrer_output_chains)
        

        # Synchronize processors
        if self.is_mpi():
            self.comm.Barrier()

        # Finish
        output_file.close()

    def prepare_gc_data(self, data) :
        '''
        Take in galaxy cluster objects, prepare for inferrer
        '''

        pass

    def make_inference(self, inferrer_input) :
        '''
        Make inference per cluster
        '''

        pass
