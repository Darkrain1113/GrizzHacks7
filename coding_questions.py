import random

class CodingQuestions:
    def __init__(self):
        self.questions = {
            1: [  # Level 1 - Basic questions
                {
                    "question": "What is the Python operator for multiplication? (type just the symbol)",
                    "answer": "*"
                },
                {
                    "question": "What is the Python operator for division? (type just the symbol)",
                    "answer": "/"
                },
                {
                    "question": "What is the Python operator for addition? (type just the symbol)",
                    "answer": "+"
                },
                {
                    "question": "What is the Python operator for subtraction? (type just the symbol)",
                    "answer": "-"
                },
                {
                    "question": "What is the Python operator for assignment? (type just the symbol)",
                    "answer": "="
                }
            ],
            2: [  # Level 2 - Intermediate questions
                {
                    "question": "What is the Python operator for integer division? (type just the symbol)",
                    "answer": "//"
                },
                {
                    "question": "What is the Python operator for modulo/remainder? (type just the symbol)",
                    "answer": "%"
                },
                {
                    "question": "What is the Python operator for exponentiation? (type just the symbol)",
                    "answer": "**"
                },
                {
                    "question": "What is the Python operator for less than? (type just the symbol)",
                    "answer": "<"
                },
                {
                    "question": "What is the Python operator for greater than? (type just the symbol)",
                    "answer": ">"
                }
            ],
            3: [  # Level 3 - Advanced questions
                {
                    "question": "What is the Python operator for less than or equal to? (type just the symbol)",
                    "answer": "<="
                },
                {
                    "question": "What is the Python operator for greater than or equal to? (type just the symbol)",
                    "answer": ">="
                },
                {
                    "question": "What is the Python operator for not equal to? (type just the symbol)",
                    "answer": "!="
                },
                {
                    "question": "What is the Python operator for equal to? (type just the symbol)",
                    "answer": "=="
                },
                {
                    "question": "What is the Python operator for logical AND? (type just the symbol)",
                    "answer": "and"
                }
            ]
        }

    def get_random_question(self, level=1):
        return random.choice(self.questions[level]) 