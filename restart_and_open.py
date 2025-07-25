import os
import subprocess
import webbrowser
import signal
import time

# Kill any running Flask server on port 5000 (Windows only)
def kill_flask():
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmd = ' '.join(proc.info['cmdline'])
                if 'aerospace_ai_tool/app.py' in cmd or 'flask' in cmd:
                    proc.kill()
    except ImportError:
        print('psutil not installed, skipping process kill.')

kill_flask()

# Wait a moment for port to free
print('Restarting server...')
time.sleep(1)


# Set only OpenRouter API key (Gemini not needed)
os.environ['OPENROUTER_API_KEY'] = "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"

# Start Flask app (ensure correct working directory)
subprocess.Popen(['python', 'aerospace_ai_tool/app.py'], cwd=os.path.dirname(os.path.abspath(__file__)))

# Wait for server to start
print('Waiting for server to start...')
time.sleep(2)

# Open in browser
webbrowser.open('http://localhost:5000')
print('Opened http://localhost:5000 in your browser.')
