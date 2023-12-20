"""
Day 34 - The Quizzler App

tags: API
"""
import html
import tkinter
import requests


THEME_COLOUR = "#375362"
FONT = ("Arial", 20, "italic")


class QuizInterface:
    """Manage the quiz graphical interface."""

    def __init__(self, quiz_brain):
        self.quiz = quiz_brain
        self.window = tkinter.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOUR)

        # Score label
        self.score_label = tkinter.Label(text="Score: 0", fg="white", bg=THEME_COLOUR)
        self.score_label.grid(column=1, row=0, sticky="E")

        # Text card
        self.canvas = tkinter.Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, 125, width=284, text="Question Text", fill=THEME_COLOUR, font=FONT
        )
        self.canvas.grid(column=0, row=1, columnspan=2, pady=20)

        # Buttons
        true_image = tkinter.PhotoImage(file="day34/images/true.png")
        self.true_button = tkinter.Button(
            image=true_image, highlightthickness=0, command=self.true_pressed
        )
        self.true_button.grid(column=0, row=2)

        false_image = tkinter.PhotoImage(file="day34/images/false.png")
        self.false_button = tkinter.Button(
            image=false_image, highlightthickness=0, command=self.false_pressed
        )
        self.false_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        """Verify if there's still questions then get the next question, reset background colour and update score."""

        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.canvas.config(bg="white")
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question_text, text="You've reached the end of the quiz."
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        """Call the check_answer function passing the True value to the give_feedback function."""

        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        """Call the check_answer function passing the False value to the give_feedback function."""

        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        """Change the background colour according to the answer and call next question."""

        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(500, self.get_next_question)


class QuizBrain:
    """Operate the quiz functionalities."""

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self) -> bool:
        """Verify whether it still has questions or not."""

        return self.question_number < len(self.question_list)

    def next_question(self) -> str:
        """Ask the next question to the user."""

        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question["text"])

        return f"Q.{self.question_number}: {q_text} (True/False): "
        # user_answer = input(f"Q.{self.question_number}: {q_text} (True/False): ")
        # self.check_answer(user_answer)

    def check_answer(self, user_answer):
        """Check the user's answer with the correct answer."""

        correct_answer = self.current_question["answer"]
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False


def get_questions():
    """Request questions from the API."""

    parameters = {
        "amount": 10,
        "type": "boolean",
    }

    response = requests.get(
        "https://opentdb.com/api.php", params=parameters, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    question_data = data["results"]

    return question_data


question_list = get_questions()
question_bank = []
for question in question_list:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = {"text": question_text, "answer": question_answer}
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

# while quiz.still_has_questions():
#    quiz.next_question()

print("You've completed the quiz!")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
