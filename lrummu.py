from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        super().__init__(frames)
        self._usage_order = []  # List to store page usage order
        self.__dirty_pages = set()  # Set to store dirty pages

    def read_memory(self, page_number):
        if page_number in self.page_table:
            # Page is in memory, update usage order
            self._update_usage_order(page_number)
            if self.debug:
                print(f"Page {page_number} read from frame {self.page_table[page_number]}")
        else:
            # Page is not in memory, page fault
            self.page_faults += 1
            self.disk_reads += 1
            self._load_page(page_number, is_write=False)
            if self.debug:
                print(f"Page fault: loaded page {page_number} (read)")

    def write_memory(self, page_number):
        self._mark_dirty(page_number)  # Mark the page as dirty
        if page_number in self.page_table:
            # Page is in memory, update usage order
            self._update_usage_order(page_number)
            if self.debug:
                print(f"Page {page_number} written to frame {self.page_table[page_number]}")
        else:
            # Page is not in memory, page fault
            self.page_faults += 1
            self.disk_reads += 1
            self._load_page(page_number, is_write=True)
            if self.debug:
                print(f"Page fault: loaded page {page_number} (write)")

    def _load_page(self, page_number, is_write):
        if len(self.page_table) < self.num_frames:
            # Free frame available, no need to evict
            frame_index = len(self.page_table)
        else:
            # Evict the least recently used page
            evicted_page = self._usage_order.pop(0)

            if self.debug:
                print(f"Evicting page {evicted_page} from frame {self.page_table[evicted_page]}")

            # Check if the evicted page is dirty and write to disk if necessary
            if self._is_dirty(evicted_page):
                self.disk_writes += 1
                if self.debug:
                    print(f"Writing dirty page {evicted_page} to disk")

                self.__dirty_pages.remove(evicted_page)  # Remove from dirty set

            frame_index = self.page_table.pop(evicted_page)

        # Load the new page into memory
        self.page_table[page_number] = frame_index
        self._usage_order.append(page_number)  # Update usage order

    def _is_dirty(self, page_number):
        return page_number in self.__dirty_pages
    
    def _mark_dirty(self, page_number):
        self.__dirty_pages.add(page_number)
        if self.debug:
            print(f"Marking page {page_number} as dirty")

    def _update_usage_order(self, page_number):
        """Move the page to the back of the usage order list (most recently used)."""
        if page_number in self._usage_order:
            self._usage_order.remove(page_number)
        self._usage_order.append(page_number)
