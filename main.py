from flask import Flask, render_template, request, jsonify, abort
import aiml
import os


# Initialize Flask app
app = Flask(__name__)



@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])

def ask():
    message = request.form['messageText'].encode('utf-8').strip()

    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
        kernel.saveBrain("bot_brain.brn")

    # Kernel now ready for use
    if message == b"quit":
        return jsonify({'status': 'error', 'answer': 'Cannot process "quit" in web context'})
    elif message == b"save":
        kernel.saveBrain("bot_brain.brn")
        return jsonify({'status': 'OK', 'answer': 'Brain saved'})
    else:
        bot_response = kernel.respond(message.decode('utf-8'))
        return jsonify({'status': 'OK', 'answer': bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
