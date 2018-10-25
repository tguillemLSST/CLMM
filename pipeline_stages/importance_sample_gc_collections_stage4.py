from ceci import PipelineStage
from descformats import TextFile, FitsFile, HDFFile, YamlFile

class ImportanceSampleGCCollectionsStage4(PipelineStage):
    '''Fourth stage of the pipeline where we importance sample chains in
each collection.

    The inputs are collections of chains, and the outputs are the
    results of importance sampling.

    The pipeline loops through the collections, and performs
    importance sampling.  Collections were defined in richness bins,
    true mass bins, etc. in the previous pipeline stage.

    It can do this in parallel if needed.  We might want to move some
    of the functionality here (e.g. the I/O) into a general parent
    class.

    '''

    name = "importance_sample_gc_collections_stage4"

    inputs = [
        ('collections_hash_table', HDFFile),# Leaving this as an
                                            # HDFFile we can perhaps
                                            # concatenate the data
                                            # into as a preprocessing
                                            # step external to the
                                            # pipeline.
        ('galaxy_cluster_chains', HDFFile)
    ]

    outputs = [
        ('importance_sampling_results', HDFFile), 
    ] # ehh... not sure how we'll want to store objects, but leaving
      # this as an HDFFile that we can un-concatenate if needed.

    config_options = {
        'galaxy_cluster_data_dir': str,  # This parameter is required in the test/config.yaml file
        'galaxy_cluster_file_type': str, # This parameter is required in the test/config.yaml file
        }

    def run(self):
        '''
        This runs importance sampling on collections (e.g. bins) of chains per cluster
        
        - Prepares the output HDF5 File
        - Loads in the chains and the hash for collections
        - Performs importance sampling
        - Writes the importance sampling chains and stats to output
        - Closes the output file

        '''

        gc_datadir = self.config['galaxy_cluster_data_dir']
        gc_filetype = self.config['galaxy_cluster_file_type']

        input_chains_file = self.open_input('galaxy_cluster_chains')
        input_hash_file = self.open_input('collections_hash_table')
        
        # Check how many objects we are running on
        ncollections = self.config['num_collections']

        input_chains_data = input_chains_file.read()
        input_chains_file.close()
        input_hash_data = input_hash_file.read()
        input_hash_file.close()
        
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
            print(f"Process {self.rank} reading in chains for rows {start}-{end}")

            # Importance sampling on each chain
            importance_sampling_output_data = self.importance_sample(data)

            # Save this chunk of data to the output file
            self.write_output(output_file, start, end, importance_sampling_output_data)
        

        # Synchronize processors
        if self.is_mpi():
            self.comm.Barrier()

        # Finish
        output_file.close()

    def importance_sample(self, data) :
        '''
        Take in collection of chains, perform importance sampling step.
        '''

        pass

