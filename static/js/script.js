let currentMode = 'object';
let audioEnabled = true;

function toggleMode() {
    fetch('/switch_mode', { method: 'POST' });
    currentMode = currentMode === 'object' ? 'face' : 'object';
    alert("Switched to " + currentMode + " mode");
}

function toggleAudio() {
    fetch('/toggle_audio', { method: 'POST' });
    audioEnabled = !audioEnabled;
    alert("Audio " + (audioEnabled ? "enabled" : "disabled"));
}

function capture() {
    fetch('/capture', { method: 'POST' });
    alert("Screenshot captured!");
}

function setCameraSource() {
    const source = prompt("Enter camera source: 'laptop' or 'ip'");
    if (source === 'ip') {
        const ip = prompt("Enter IP Webcam address (e.g. 192.168.1.100:8080)");
        if (ip) {
            fetch('/set_camera_source', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source: 'ip', ip: ip })
            })
            .then(response => response.json())
            .then(data => alert(data.status));
        }
    } else {
        fetch('/set_camera_source', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source: 'laptop' })
        })
        .then(response => response.json())
        .then(data => alert(data.status));
    }
}