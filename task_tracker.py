from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

tasks = []
completed_tasks = []

patterns = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm good, thanks!", "I'm doing well.", "I'm fine, how about you?"],
    "what's your name": ["I'm a chatbot.", "You can call me Chatbot.", "I don't have a name."],
    "bye": ["Goodbye!", "Bye bye!", "Take care!"],
    "add task": ["Sure, what's the task?", "What task would you like to add?", "Tell me the task you want to add."],
    "complete task": ["Which task would you like to mark as complete?", "Which task have you finished?", "Let me know the task you want to complete."],
    "show tasks": ["Here are your current tasks:", "These are the tasks you need to do:", "Your tasks are:"]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input'].lower()

        response = process_user_input(user_input)
        return jsonify({'message': response})

    return render_template('index.html', tasks=tasks, completed_tasks=completed_tasks)


def process_user_input(user_input):
    for pattern, responses in patterns.items():
        if any(keyword in user_input for keyword in pattern.split('|')):
            return get_random_response(responses)

    if user_input.startswith('add') or user_input.startswith('create'):
        task = user_input.replace('add', '').replace('create', '').strip()
        tasks.append(task)
        return f"Task '{task}' has been added."

    elif user_input.startswith('complete') or user_input.startswith('finished'):
        task = user_input.replace('complete', '').replace('finished', '').strip()
        if task in tasks:
            tasks.remove(task)
            completed_tasks.append(task)
            return f"Task '{task}' has been marked as complete."
        else:
            return f"Task '{task}' not found."

    elif user_input.startswith('show'):
        return '\n'.join(tasks) if tasks else 'You have no tasks.'

    return "I'm sorry, I didn't understand that."


def get_random_response(responses):
    import random
    return random.choice(responses)


if __name__ == '__main__':
    app.run()
