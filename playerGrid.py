class PlayerGrid:
    def __init__(self):
        
        self.rows = 3  
        self.cols = 3 
        self.grid = []  # an empty grid

        # 3x3 grid filled with 0s
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(0)
            self.grid.append(row)