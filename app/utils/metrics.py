from sklearn.metrics import mean_squared_error, precision_score, recall_score
import numpy as np

class RecommendationMetrics:
    @staticmethod
    def calculate_rmse(true_ratings, predicted_ratings):
        return np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
    
    @staticmethod
    def calculate_precision_at_k(true_positives, false_positives, k=10):
        if true_positives + false_positives == 0:
            return 0.0
        return true_positives / (true_positives + false_positives)
    
    @staticmethod
    def calculate_recall_at_k(true_positives, false_negatives, k=10):
        if true_positives + false_negatives == 0:
            return 0.0
        return true_positives / (true_positives + false_negatives)