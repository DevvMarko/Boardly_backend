from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# init flask
app = Flask(__name__)

# configure connection to database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init database
db = SQLAlchemy(app)


class Tasks(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    task_description = db.Column(db.String(255))
    task_icon = db.Column(db.String(20))
    task_status = db.Column(db.String(20))
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id'), nullable=False)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_description": self.task_description,
            "task_icon": self.task_icon,
            "task_status": self.task_status,
            "board_id": self.board_id
        }


class Boards(db.Model):
    __tablename__ = 'boards'
    board_id = db.Column(db.Integer, primary_key=True)
    board_name = db.Column(db.String(255))
    board_description = db.Column(db.String(255))

    def to_dict(self):
        return {
            "board_id": self.board_id,
            "board_name": self.board_name,
            "board_description": self.board_description
        }


# get tasks by board id
@app.route('/api/boards/<int:board_id>', methods=['GET'])
def get_board_data(board_id):
    # Query for the board and its tasks
    # We join them to ensure the board exists and to get board details
    results = db.session.query(
        Boards.board_id,
        Boards.board_name,
        Boards.board_description,
        Tasks.task_id,
        Tasks.task_name,
        Tasks.task_description,
        Tasks.task_icon,
        Tasks.task_status
    ).join(Boards, Tasks.board_id == Boards.board_id).filter(Tasks.board_id == board_id).all()

    if not results:
        # If no tasks found, maybe the board exists but is empty? 
        # Or the board doesn't exist. Let's check for the board specifically.
        board = Boards.query.get(board_id)
        if not board:
            return jsonify({"error": "Board not found"}), 404
        
        return jsonify({
            **board.to_dict(),
            "tasks": []
        })

    # Prepare a structured response
    # We take board info from the first row and collect tasks
    first_row = results[0]
    data = {
        "board_id": first_row.board_id,
        "board_name": first_row.board_name,
        "board_description": first_row.board_description,
        "tasks": [
            {
                "task_id": r.task_id,
                "task_name": r.task_name,
                "task_description": r.task_description,
                "task_icon": r.task_icon,
                "task_status": r.task_status,
            }
            for r in results
        ]
    }

    return jsonify(data)

# update board data
@app.route('/api/boards/<int:board_id>', methods=['PUT'])
def update_board_data(board_id):
    board = Boards.query.get(board_id)
    if not board:
        return jsonify({"error": "Board not found"}), 404
    data = request.json
    board.board_name = data.get('board_name', board.board_name)
    board.board_description = data.get('board_description', board.board_description)
    db.session.commit()
    return jsonify(board.to_dict())

# create new board
@app.route('/api/boards', methods=['POST'])

#delete board
@app.route('/api/boards/<int:board_id>', methods=['DELETE'])
def delete_board(board_id):
    board = Boards.query.get(board_id)
    if not board:
        return jsonify({"error": "Board not found"}), 404
    db.session.delete(board)
    db.session.commit()
    return jsonify(board.to_dict())

# create new task
@app.route('/api/boards/<int:board_id>', methods=['POST'])

# update task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Tasks.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    task.task_name = data.get('task_name', task.task_name)
    task.task_description = data.get('task_description', task.task_description)
    task.task_icon = data.get('task_icon', task.task_icon)
    task.task_status = data.get('task_status', task.task_status)
    db.session.commit()
    return jsonify(task.to_dict())

# delete task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify(task.to_dict())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Run the backend server.")
    parser.add_argument('--dev', action='store_true', help='Run in development mode')
    args = parser.parse_args()

    if args.dev:
        print("Starting development server...")
        app.run(debug=True)
    else:
        print("Starting production server with Waitress...")
        try:
            from waitress import serve
            serve(app, host='0.0.0.0', port=5000)
        except ImportError:
            print("Waitress is not installed. Falling back to development server...")
            app.run()
