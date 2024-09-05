from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        super().__init__(frames)
        # TODO: Constructor logic for LruMMU
        self._usage_order = [] # List to store page usage order
        self._dirty_pages = set() # Set to store dirty pages
        pass

    def read_memory(self, page_number):
        if page_number in self.page_table:
            # Page is in memory
            if self.debug:
                print(f"Page {page_number} read from frame {self.page_table[page_number]}")
        else:
            # Page is not in memory
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


    def _load_page(self, page_number):
        if len(self.page_table) < self.num_frames:
            # Free frame available, no need to evict
            frame_index = len(self.page_table)
            self._usage_order.append(page_number)
        else:
            # Evict the least recently used page
            evicted_page = self._usage_order.pop(0)
            self._mark_dirty(evicted_page)
            if self.debug:
                print(f"Evicting page {evicted_page} from frame {self.page_table[evicted_page]}")
            
            if self._is_dirty(evicted_page):
                self.disk_writes += 1
                if self.debug:
                    print(f"Writing dirty page {evicted_page} to disk")

            frame_index = self.page_table[evicted_page]
            self.page_table.pop(evicted_page)
            self._usage_order.append(page_number)
        self.page_table[page_number] = frame_index

    def _is_dirty(self, page_number):
        return page_number in self._dirty_pages
    
    def _mark_dirty(self, page_number):
        self._dirty_pages.add(page_number)
        if self.debug:
            print(f"Marking page {page_number} as dirty")

