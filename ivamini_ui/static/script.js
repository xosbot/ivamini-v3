/**
 * IVAmini UI — Client-side interaction script
 * All logic remains server-side in ivamini.orchestrator
 */

/**
 * Execute a task by calling the backend API
 */
async function executeTask() {
    const mode = document.getElementById('mode').value;
    const content = document.getElementById('content').value.trim();

    if (!content) {
        alert('Please enter some text');
        return;
    }

    // Show loading indicator
    showLoading(true);
    clearOutput();

    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mode: mode,
                content: content
            })
        });

        const data = await response.json();

        if (data.status === 'ERROR') {
            displayError(data.error);
        } else {
            displayResult(data);
        }
    } catch (error) {
        displayError(`Network error: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * Display task result
 */
function displayResult(result) {
    const outputBox = document.getElementById('output');
    
    if (result.result && result.result.raw_output) {
        // Structured LLM output
        outputBox.textContent = result.result.raw_output;
    } else if (result.result && result.result.entries) {
        // MEMORY response
        const entries = result.result.entries;
        if (entries.length === 0) {
            outputBox.textContent = '(No memory entries)';
        } else {
            const formatted = entries
                .map(e => `[${e.type}] ${e.content}\n    (${new Date(e.time).toLocaleTimeString()})`)
                .join('\n\n');
            outputBox.textContent = formatted;
        }
    } else if (result.result) {
        // Other structured responses
        outputBox.textContent = JSON.stringify(result.result, null, 2);
    } else {
        outputBox.textContent = '(No output)';
    }
    
    outputBox.classList.remove('placeholder');
}

/**
 * Display error message
 */
function displayError(message) {
    const outputBox = document.getElementById('output');
    outputBox.textContent = `ERROR: ${message}`;
    outputBox.classList.add('error');
}

/**
 * Clear output display
 */
function clearOutput() {
    const outputBox = document.getElementById('output');
    outputBox.textContent = 'Processing...';
    outputBox.classList.remove('error', 'success');
    outputBox.classList.add('placeholder');
}

/**
 * Clear input
 */
function clearInput() {
    document.getElementById('content').value = '';
    document.getElementById('content').focus();
}

/**
 * Load and display system status
 */
async function loadStatus() {
    const statusBox = document.getElementById('status-info');
    statusBox.textContent = 'Loading status...';

    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        if (data.status === 'ERROR') {
            statusBox.textContent = `ERROR: ${data.error}`;
            statusBox.parentElement.classList.add('error');
        } else {
            const status = data.result || data;
            const formatted = formatStatus(status);
            statusBox.textContent = formatted;
            statusBox.parentElement.classList.remove('error');
        }
    } catch (error) {
        statusBox.textContent = `Network error: ${error.message}`;
        statusBox.parentElement.classList.add('error');
    }
}

/**
 * Load and display session memory
 */
async function loadMemory() {
    const memoryBox = document.getElementById('memory-info');
    memoryBox.textContent = 'Loading memory...';

    try {
        const response = await fetch('/api/memory');
        const data = await response.json();

        if (data.status === 'ERROR') {
            memoryBox.textContent = `ERROR: ${data.error}`;
            memoryBox.parentElement.classList.add('error');
        } else {
            const memory = data.result || data;
            const entries = memory.entries || [];
            
            if (entries.length === 0) {
                memoryBox.textContent = '(No memory entries yet)';
            } else {
                const formatted = entries
                    .map((e, i) => `[${i + 1}] ${e.type}\n${e.content}\n(${new Date(e.time).toLocaleTimeString()})`)
                    .join('\n' + '─'.repeat(50) + '\n');
                memoryBox.textContent = formatted;
            }
            memoryBox.parentElement.classList.remove('error');
        }
    } catch (error) {
        memoryBox.textContent = `Network error: ${error.message}`;
        memoryBox.parentElement.classList.add('error');
    }
}

/**
 * Restart session (clear memory and create new orchestrator)
 */
async function restartSession() {
    if (!confirm('Are you sure you want to restart the session? This will clear all memory.')) {
        return;
    }

    try {
        const response = await fetch('/api/restart', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.status === 'SUCCESS') {
            alert('Session restarted successfully');
            clearInput();
            clearOutput();
            document.getElementById('memory-info').textContent = '(Memory cleared)';
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Network error: ${error.message}`);
    }
}

/**
 * Switch between tabs
 */
function switchTab(tabId, button) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Deactivate all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabId).classList.add('active');

    // Activate button
    button.classList.add('active');

    // Load data if needed
    if (tabId === 'status-tab') {
        loadStatus();
    } else if (tabId === 'memory-tab') {
        loadMemory();
    }
}

/**
 * Show/hide loading indicator
 */
function showLoading(show) {
    const indicator = document.getElementById('status-indicator');
    if (show) {
        indicator.style.display = 'flex';
    } else {
        indicator.style.display = 'none';
    }
}

/**
 * Format status object for display
 */
function formatStatus(status) {
    const items = [];
    for (const [key, value] of Object.entries(status)) {
        if (typeof value === 'object') {
            items.push(`${key}: ${JSON.stringify(value)}`);
        } else {
            items.push(`${key}: ${value}`);
        }
    }
    return items.join('\n');
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Focus input on load
    document.getElementById('content').focus();

    // Allow Ctrl+Enter to submit
    document.getElementById('content').addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            executeTask();
        }
    });
});
