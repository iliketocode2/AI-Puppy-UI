document.addEventListener('DOMContentLoaded', function() {
    //change colors of download block and sensor data block
    const connectButton = document.getElementById('connect-spike');
    const downloadButton = document.getElementById('download-code');
    const sensorButton = document.getElementById('sensor_readings');
    const runButton = document.getElementById('custom-run-button');

    function setButtonState(button, isActive) {
        if (isActive) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    }

    function updateButtonStates(isConnected, isSensorMode) {
        setButtonState(downloadButton, isConnected && !isSensorMode);
        setButtonState(sensorButton, isConnected);
        setButtonState(runButton, isConnected && !isSensorMode);
    }

    // Initial state
    updateButtonStates(false, false);

    // Connect button click handler
    connectButton.addEventListener('click', function() {
        const isConnected = !this.classList.contains('connected');
        this.classList.toggle('connected');
        this.textContent = isConnected ? 'Connected!' : 'Connect Spike Prime';
        updateButtonStates(isConnected, false);
    });

    // Sensor button click handler
    sensorButton.addEventListener('click', function() {
        if (this.classList.contains('active')) {
            const isSensorMode = this.textContent === 'Sensor Readings';
            this.textContent = isSensorMode ? 'Get Terminal' : 'Sensor Readings';
            updateButtonStates(true, isSensorMode);
        }
    });

    //connect js button to mpy-editor
    document.getElementById('custom-run-button').addEventListener('click', function() {
   
        const editor = document.getElementById(this.getAttribute('data-editor-id'));
        if (editor) {
            const event = new CustomEvent('mpy-run', {
                bubbles: true,
                detail: { code: editor.code }
            });
            editor.dispatchEvent(event);
        }
    });

    // Code for resizable terminal
    let topBox = document.querySelector('.right-box:first-child');
    let bottomBox = document.getElementById("resizeBox");
    let slider = document.querySelector(".slider");
    let container = document.querySelector('.right-container');

    let startY;
    let startTopHeight;
    let startBottomHeight;

    slider.addEventListener('mousedown', initDrag, false);

    function initDrag(e) {
        startY = e.clientY;
        startTopHeight = topBox.offsetHeight;
        startBottomHeight = bottomBox.offsetHeight;
        
        document.documentElement.addEventListener('mousemove', doDrag, false);
        document.documentElement.addEventListener('mouseup', stopDrag, false);
    }

    function doDrag(e) {
        let newTopHeight = startTopHeight + e.clientY - startY;
        let newBottomHeight = startBottomHeight - (e.clientY - startY);

        if (newTopHeight > 50 && newBottomHeight > 50) {
            topBox.style.height = newTopHeight + 'px';
            bottomBox.style.height = newBottomHeight + 'px';
        }
    }

    function stopDrag() {
        document.documentElement.removeEventListener('mousemove', doDrag, false);
        document.documentElement.removeEventListener('mouseup', stopDrag, false);
    }
});