import logging
import numpy as np
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

class MLService:
    """
    Machine Learning service for predicting knowledge retention and enabling spaced repetition.
    """
    def __init__(self):
        # We use a simple Logistic Regression model for predicting retention probability.
        self.model = LogisticRegression()
        self.is_trained = False
        
        # In a real production system, this model would be trained asynchronously 
        # on historical database records and the weights saved/loaded.
        # For this implementation, we'll initialize it with a sensible baseline.
        self._initialize_baseline_model()

    def _initialize_baseline_model(self):
        """
        Trains the model on synthetic baseline data so it can make reasonable 
        predictions immediately before enough real user data is collected.
        """
        # Features: [mastery_score, attempts_to_mastery, days_since_last_review, difficulty]
        X = np.array([
            [1.0, 1, 1, 2],    # Perfect score, 1 attempt, 1 day ago, easy -> Retained
            [0.9, 2, 7, 5],    # High score, 2 attempts, 7 days ago, medium -> Retained
            [0.8, 1, 30, 8],   # Good score, 1 attempt, 30 days ago, hard -> Forgotten
            [0.6, 4, 14, 9],   # Low score, 4 attempts, 14 days ago, very hard -> Forgotten
            [1.0, 1, 60, 5],   # Perfect score, 1 attempt, 60 days ago, medium -> Forgotten (decay)
            [0.9, 3, 2, 8]     # High score, 3 attempts, 2 days ago, hard -> Retained
        ])
        
        # Targets: 1 = Retained, 0 = Forgotten
        y = np.array([1, 1, 0, 0, 0, 1])
        
        self.model.fit(X, y)
        self.is_trained = True
        logger.info("MLService initialized with baseline retention model.")

    def predict_retention(
        self, 
        mastery_score: float, 
        attempts_to_mastery: int, 
        days_since_last_review: float, 
        difficulty: int
    ) -> float:
        """
        Predicts the probability (0.0 to 1.0) that the user currently remembers the topic.
        """
        if not self.is_trained:
            logger.warning("Retention model called before training. Returning default 1.0")
            return 1.0
            
        features = np.array([[mastery_score, attempts_to_mastery, days_since_last_review, difficulty]])
        
        # predict_proba returns [[prob_0, prob_1]]
        probability = self.model.predict_proba(features)[0][1]
        
        return float(probability)
        
    def needs_review(self, probability: float, threshold: float = 0.75) -> bool:
        """
        Determines if a topic needs review based on the retention probability.
        """
        return probability < threshold

ml_service = MLService()
