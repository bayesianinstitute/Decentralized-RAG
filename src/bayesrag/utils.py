from enum import Enum

class ClassificationResult(Enum):
    """
    a ClassificationResult enum.

    Returns:
        ClassificationResult.YES if the query is classified as a law-related question, 
        ClassificationResult.NO if it's not a law-related question, 
        ClassificationResult.ERROR if there's an error parsing the response.
    """
    
    YES = "yes"
    NO = "no"
    ERROR = "error"