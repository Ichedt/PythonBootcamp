"""
Day 17 - Quiz Game

tags: classes, initialization
"""

question_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The loudest animal is the African Elephant.", "answer": "False"},
    {
        "text": "Approximately one quarter of human bones are in the feet.",
        "answer": "True",
    },
    {
        "text": "The total surface area of a human lungs is the size of a "
        "football pitch.",
        "answer": "True",
    },
    {
        "text": "In West Virginia, USA, if you accidentally hit an animal "
        "with your car, you are free to take it home to eat.",
        "answer": "True",
    },
    {
        "text": "In London, UK, if you happen to die in the House of "
        "Parliament, you are entitled to a state funeral.",
        "answer": "False",
    },
    {"text": "It is illegal to pee in the Ocean in Portugal.", "answer": "True"},
    {"text": "You can lead a cow down stairs but not up stairs.", "answer": "False"},
    {"text": "Google was originally called 'Backrub'.", "answer": "True"},
    {"text": "Buzz Aldrin's mother's maiden name was 'Moon'.", "answer": "True"},
    {
        "text": "No piece of square dry paper can be folded in half more than 7 "
        "times.",
        "answer": "False",
    },
    {"text": "A few ounces of chocolate can to kill a small dog.", "answer": "True"},
]


class Question:
    """Question constructor."""

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer


class QuizBrain:
    """Processes questions, answers and score."""

    def __init__(self, questions_list):
        self.question_number = 0
        self.score = 0
        self.questions_list = questions_list

    def still_has_questions(self):
        """Returns True or False wether if it still has questions."""
        return self.question_number < len(self.questions_list)

    def next_question(self):
        """Gets the current question and shows the next question."""
        current_question = self.questions_list[self.question_number]
        self.question_number += 1
        user_answer = input(
            f"Q.{self.question_number}: {current_question.text} (True/False): "
        )
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        """Checks if the question is correct and adds up the score."""
        if user_answer.lower() == correct_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong.")
            print(f"The correct answer was: {correct_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number}.")
        print("\n")


if __name__ == "__main__":
    question_bank = []
    for question in question_data:
        question_text = question["text"]
        question_answer = question["answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)

    while quiz.still_has_questions():
        quiz.next_question()

    print("You've completed the quiz!")
    print(f"Your final score was: {quiz.score}/{quiz.question_number}!")
