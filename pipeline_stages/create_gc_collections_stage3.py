from ceci import PipelineStage
from descformats import TextFile, FitsFile, HDFFile, YamlFile

class CreateGCCollectionsStage3(PipelineStage):
    '''Third stage of the pipeline where we define the binning of for
importance sampling.

    The inputs are galaxy cluster data with individual chains per
    cluster, and the outputs are the collections of cluster chains.

    The pipeline loops through galaxy cluster objects and identifies
    which collection they belong to.  Collections can be defined in
    richness bins, true mass bins, etc.

    It can do this in parallel if needed.  We might want to move some
    of the functionality here (e.g. the I/O) into a general parent
    class.

    '''

    name = "create_gc_collections_stage3"

    inputs = [
        ('galaxy_cluster_objects_with_chains', HDFFile), # Leaving this as an
                                            # HDFFile we can perhaps
                                            # concatenate the data
                                            # into as a preprocessing
                                            # step external to the
                                            # pipeline.
    ]

    outputs = [
        ('collections_hash_table', HDFFile), 
    ]
    
    config_options = {
        'galaxy_cluster_data_dir': str,  # This parameter is required in the test/config.yaml file
        'galaxy_cluster_file_type': str, # This parameter is required in the test/config.yaml file
        'num_collections': int, # This parameter is required in the test/config.yaml file
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
        - Defines collections of galaxy clusters (e.g. binning)
        - Writes the collections hash table to output
        - Closes the output file

        '''

        gc_datadir = self.config['galaxy_cluster_data_dir']
        gc_filetype = self.config['galaxy_cluster_file_type']

        input_file = self.open_input('galaxy_clusters_input')

        # Check how many objects we are running on
        ngalaxyclusters = self.get_num_clusters(input_file)
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
            print(f"Process {self.rank} reading in galaxy cluster objects with chains for rows {start}-{end}")

            # Populate galaxy cluster objects
            collections_hash_table = self.populate_collections(data)

            # Save this chunk of data to the output file
            self.write_output(output_file, start, end, collections_hash_table)
        

        # Synchronize processors
        if self.is_mpi():
            self.comm.Barrier()

        # Finish
        output_file.close()

    def populate_collections(self, data) :
        '''
        Take in galaxy cluster data, collect the information needed to create collections (e.g. richness, true mass, etc.)
        '''

        pass

