class Submission:
    def __init__(self,
                 problem_number = None,
                 answer = None,
                 language = None,
                 total_lines = None,
                 total_runtime = None):
        self.problem_number = problem_number
        self.answer = answer
        self.language = language
        self.total_lines = total_lines
        self.total_runtime = total_runtime