class tree:
    def __init__(self, features, visited, results, indexes, depth, currentLevelPrediction, boolean):
        self.features = features
        self.visited = visited
        self.results = results
        self.indexes = indexes
        self.depth = depth
        self.currentLevelPrediction = currentLevelPrediction
        self.bool = boolean
        self.value = None
        self.left = None
        self.right = None
