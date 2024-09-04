import random
from mmu import MMU

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames  # Number of page frames
        self.page_table = {}  # Maps page number to frame index
        self.frame_list = []  # List of page numbers in memory
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        if page_number in self.page_table:
            if self.debug:
                print(f"Page {page_number} read from frame {self.page_table[page_number]}")
        else:
            self.page_faults += 1
            self.disk_reads += 1
            self._load_page(page_number)
            if self.debug:
                print(f"Page fault: loaded page {page_number}")

    def write_memory(self, page_number):
        if page_number in self.page_table:
            if self.debug:
                print(f"Page {page_number} written to frame {self.page_table[page_number]}")
        else:
            self.page_faults += 1
            self.disk_reads += 1
            self._load_page(page_number)
            if self.debug:
                print(f"Page fault: loaded page {page_number} (write)")


        self._mark_dirty(page_number)

    def _load_page(self, page_number):
        if len(self.frame_list) < self.frames:
            
            frame_index = len(self.frame_list)
            self.frame_list.append(page_number)
        else:

            evict_index = random.randint(0, self.frames - 1)
            evicted_page = self.frame_list[evict_index]
            if self.debug:
                print(f"Evicting page {evicted_page} from frame {evict_index}")
            
            if self._is_dirty(evicted_page):
                self.disk_writes += 1
                if self.debug:
                    print(f"Writing dirty page {evicted_page} to disk")

            self.page_table.pop(evicted_page)
            self.frame_list[evict_index] = page_number
            frame_index = evict_index

        self.page_table[page_number] = frame_index

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults

    def _mark_dirty(self, page_number):
        if self.debug:
            print(f"Page {page_number} marked as dirty")

    def _is_dirty(self, page_number):
        # Placeholder for checking if a page is dirty
        # Assuming all pages written to are dirty
        return True
