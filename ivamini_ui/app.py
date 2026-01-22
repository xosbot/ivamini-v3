"""
IVAmini UI — Thin Flask client for core reasoning engine.

All logic remains in ivamini.orchestrator.core.
This is a read-only display layer.
"""

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sys

# Add parent directory to path so we can import ivamini
sys.path.insert(0, str(Path(__file__).parent.parent))

from ivamini.orchestrator.core import Orchestrator
from ivamini.config import load_config

app = Flask(__name__)
orchestrator = Orchestrator()
config = load_config()

# Store session in app context
session_id = None


@app.route('/')
def index():
    """Main UI page"""
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def api_status():
    """Get system status"""
    try:
        task = orchestrator.create_task("STATUS", "STATUS", "")
        result = orchestrator.execute_task(task)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500


@app.route('/api/memory', methods=['GET'])
def api_memory():
    """Get session memory"""
    try:
        task = orchestrator.create_task("MEMORY", "MEMORY", "")
        result = orchestrator.execute_task(task)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500


@app.route('/api/execute', methods=['POST'])
def api_execute():
    """
    Execute a task.
    
    Request JSON:
    {
        "mode": "QUESTION|REVIEW|PLAN",
        "content": "User input text"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'mode' not in data or 'content' not in data:
            return jsonify({
                "status": "ERROR",
                "error": "Missing 'mode' or 'content' in request"
            }), 400
        
        mode = data['mode'].upper()
        content = data['content'].strip()
        
        if not content:
            return jsonify({
                "status": "ERROR",
                "error": "Content cannot be empty"
            }), 400
        
        # Validate mode
        if mode not in ["QUESTION", "REVIEW", "PLAN"]:
            return jsonify({
                "status": "ERROR",
                "error": f"Invalid mode: {mode}. Use QUESTION, REVIEW, or PLAN"
            }), 400
        
        # Create and execute task
        task = orchestrator.create_task(mode, mode, content)
        result = orchestrator.execute_task(task)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500


@app.route('/api/restart', methods=['POST'])
def api_restart():
    """
    Restart session (clear memory).
    Creates a new Orchestrator instance.
    """
    global orchestrator
    
    try:
        orchestrator = Orchestrator()
        return jsonify({
            "status": "SUCCESS",
            "message": "Session restarted"
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "ERROR",
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "ERROR",
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("IVAmini UI — Flask Local Interface")
    print("="*60)
    print(f"Environment: {config.get('environment', 'unknown')}")
    print(f"LLM Model: {config.get('llm', {}).get('model', 'unknown')}")
    print("\nStarting Flask server...")
    print("Open browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(
        debug=False,
        host='127.0.0.1',
        port=5000,
        use_reloader=False
    )
