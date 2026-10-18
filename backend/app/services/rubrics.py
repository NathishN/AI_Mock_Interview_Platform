"""Default rubrics from the product spec. Weights sum to 100 per rubric."""

DEFAULT_RUBRICS: dict[str, dict] = {
    "technical": {
        "name": "Technical interview",
        "dimensions": [
            {"name": "Technical correctness", "weight": 35},
            {"name": "Completeness", "weight": 20},
            {"name": "Clarity", "weight": 15},
            {"name": "Relevance", "weight": 15},
            {"name": "Reasoning", "weight": 15},
        ],
    },
    "hr": {
        "name": "HR interview",
        "dimensions": [
            {"name": "Relevance", "weight": 20},
            {"name": "Answer structure", "weight": 20},
            {"name": "Specificity and supporting examples", "weight": 20},
            {"name": "Self-awareness", "weight": 15},
            {"name": "Professional communication", "weight": 15},
            {"name": "Authenticity and consistency", "weight": 10},
        ],
    },
    "coding": {
        "name": "Coding question",
        "dimensions": [
            {"name": "Functional correctness", "weight": 40},
            {"name": "Algorithmic reasoning", "weight": 20},
            {"name": "Complexity analysis", "weight": 15},
            {"name": "Edge-case handling", "weight": 15},
            {"name": "Explanation", "weight": 10},
        ],
    },
}
