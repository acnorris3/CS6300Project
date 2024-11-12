class Metrics:
    def __init__(self, squares_per_battery=50, total_squares_in_lawn=100):
        """
        Initialize the metrics object with default values.

        :param squares_per_battery: The number of squares that can be mowed with a full battery.
        """
        self.metrics = {
            'seen': 0, # How many squares the mower has been over
            'mowed': 0, # How many squares the mower has cut
            'collisions': 0, # How many collisions the mower has had with objects (trees, rocks, etc.)
            'overlap': 0, # How many times the mower has overlapped with its own path
            'battery': 100 # The current battery level of the mower
        }
        self.squares_per_battery = squares_per_battery
        self.total_squares_in_lawn = total_squares_in_lawn

    def get_metrics(self):
        """
        Return the metrics of the mower
        """
        return self.metrics

    def add_mowed(self):
        """
        Increment the number of mowed squares and seen squares, and decrement the battery
        """
        self.metrics['mowed'] += 1
        self.metrics['seen'] += 1
        self.metrics['battery'] -= 100 / self.squares_per_battery
    
    def add_overlap(self):
        """
        Increment the number of overlapped squares and seen squares, and decrement the battery
        """
        self.metrics['overlap'] += 1
        self.metrics['seen'] += 1
        self.metrics['battery'] -= 100 / self.squares_per_battery

    def add_collision(self):
        """
        Increment the number of collisions.
        
        At the time of writing I envision we are not letting the mower move if it encounters a collision, 
        the battery does not decrement, the mower does not mow the square, and the mower does not increment the number of seen squares.
        """
        self.metrics['collisions'] += 1

    def set_battery(self, battery):
        """
        Set the battery level of the mower
        """
        self.metrics['battery'] = battery

    def get_battery(self):
        """
        Return the battery level of the mower
        """
        return self.metrics['battery']

    def reset(self):
        """
        Reset the metrics to their default values
        """
        self.metrics = {
            'seen': 0,
            'mowed': 0,
            'collisions': 0,
            'overlap': 0,
            'battery': 100
        }

    def calculate_efficiency_ratio(self):
        """
        Calculate the efficiency ratio of the mower: mowed / seen
        """
        if self.metrics['seen'] == 0:
            return 0
        return self.metrics['mowed'] / self.metrics['seen']
    
    def calculate_coverage_ratio(self):
        """
        Calculate the coverage ratio of the mower: mowed / total_squares_in_lawn
        """
        if self.total_squares_in_lawn == 0:
            return 0
        return self.metrics['mowed'] / self.total_squares_in_lawn
    
    def calculate_overlap_vs_mowed(self):
        """
        Calculate the overlap rate of the mower: overlap / mowed
        """
        if self.metrics['mowed'] == 0:
            return 0
        return self.metrics['overlap'] / self.metrics['mowed']
    
    def calcualte_overlap_vs_seen(self):
        """
        Calculate the overlap rate of the mower: overlap / seen
        """
        if self.metrics['seen'] == 0:
            return 0
        return self.metrics['overlap'] / self.metrics['seen']