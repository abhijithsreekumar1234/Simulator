'''
* Interface for Memory Management Unit.
* The memory management unit should maintain the concept of a page table.
* As pages are read and written to, this changes the pages loaded into the
* the limited number of frames. The MMU keeps records, which will be used
* to analyse the performance of different replacement strategies implemented
* for the MMU.
*
'''
class MMU:
    def __init__(self, frames):
        self.num_frames = frames  # Number of page frames
        self.page_table = {}  # Maps page number to frame index
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def read_memory(self, page_number):
        pass

    def write_memory(self, page_number):
        pass

    def set_debug(self):
        # Set debug mode
        self.debug = True

    def reset_debug(self):
        # Disable debug mode
        self.debug = False

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
