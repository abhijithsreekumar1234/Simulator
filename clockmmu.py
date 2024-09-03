from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):

        # Initialize the ClockMMU with the given number of frames.

        self.num_frames = frames
        self.frames = [None] * frames  # List to store page information
        self.clock_hand = 0  # Pointer for clock algorithm
        self.page_table = {}  # Maps page_number to frame index
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):

        # Enable debug mode.

        self.debug = True

    def reset_debug(self):

        # Disable debug mode.

        self.debug = False

    def read_memory(self, page_number):

        # Handle memory read operation for the given page number.

        if page_number in self.page_table:
            frame_index = self.page_table[page_number]
            frame = self.frames[frame_index]
            frame['reference_bit'] = 1
            if self.debug:
                print(f"Read hit: Page {page_number} is already in frame {frame_index}.")
        else:
            if self.debug:
                print(f"Read miss: Page {page_number} not in memory. Page fault occurs.")
            self.page_faults += 1
            self._load_page(page_number, is_write=False)

    def write_memory(self, page_number):

        # Handle memory write operation for the given page number.

        if page_number in self.page_table:
            frame_index = self.page_table[page_number]
            frame = self.frames[frame_index]
            frame['reference_bit'] = 1
            frame['dirty_bit'] = 1
            if self.debug:
                print(f"Write hit: Page {page_number} is already in frame {frame_index}. Dirty bit set.")
        else:
            if self.debug:
                print(f"Write miss: Page {page_number} not in memory. Page fault occurs.")
            self.page_faults += 1
            self._load_page(page_number, is_write=True)

    def _load_page(self, page_number, is_write):

        # Load the page into memory using the clock replacement algorithm.

        # Check if there is a free frame available
        for i in range(self.num_frames):
            if self.frames[i] is None:
                self.frames[i] = {
                    'page_number': page_number,
                    'reference_bit': 1,
                    'dirty_bit': 1 if is_write else 0
                }
                self.page_table[page_number] = i
                self.disk_reads += 1
                if self.debug:
                    print(f"Loading page {page_number} into free frame {i}.")
                return

        # No free frame found; use clock algorithm to find victim
        while True:
            frame = self.frames[self.clock_hand]
            if frame['reference_bit'] == 0:
                # Victim found
                victim_page = frame['page_number']
                if frame['dirty_bit'] == 1:
                    self.disk_writes += 1
                    if self.debug:
                        print(f"Evicting dirty page {victim_page} from frame {self.clock_hand}. Writing to disk.")
                else:
                    if self.debug:
                        print(f"Evicting clean page {victim_page} from frame {self.clock_hand}.")
                # Remove victim page from page table
                del self.page_table[victim_page]
                # Replace with new page
                self.frames[self.clock_hand] = {
                    'page_number': page_number,
                    'reference_bit': 1,
                    'dirty_bit': 1 if is_write else 0
                }
                self.page_table[page_number] = self.clock_hand
                self.disk_reads += 1
                if self.debug:
                    print(f"Loading page {page_number} into frame {self.clock_hand}.")
                # Move clock hand forward
                self.clock_hand = (self.clock_hand + 1) % self.num_frames
                break
            else:
                # Give second chance
                frame['reference_bit'] = 0
                if self.debug:
                    print(f"Second chance given to page {frame['page_number']} in frame {self.clock_hand}.")
                self.clock_hand = (self.clock_hand + 1) % self.num_frames

    def get_total_disk_reads(self):

        # Return the total number of disk reads.

        return self.disk_reads

    def get_total_disk_writes(self):

        # Return the total number of disk writes.

        return self.disk_writes

    def get_total_page_faults(self):

        # Return the total number of page faults.

        return self.page_faults
