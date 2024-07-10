document.addEventListener('DOMContentLoaded', function() {
    //change colors of download block and sensor data block
    const connectButton = document.getElementById('connect-spike');
    const downloadButton = document.getElementById('download-code');
    const sensorButton = document.getElementById('sensor_readings');
    const runButton = document.getElementById('custom-run-button');


     //JAV-CODE (below)
    window.checkCurrentLesson = checkCurrentLesson;
    function checkCurrentLesson() {
        // Get the ID of the body element
        var currentLesson = document.body.id;

        //hide mpy editor for lesson 1 and 2
        if (currentLesson === 'lesson1' || currentLesson === 'lesson2'){
            document.getElementById('hide_on_1_and_2').style.display = 'none';
        }
        else{
            document.getElementById('hide_on_1_and_2').style.display = 'block';
        }

        // Use the currentLesson variable to determine which lesson you are in
        switch (currentLesson) {
            case "lesson1":
                console.log("JS:You are in Lesson 1");
                // Additional actions specific to Lesson 1
                return 1;
            case "lesson2":
                console.log("JS:You are in Lesson 2");
                // Additional actions specific to Lesson 2
                return 2;
            case "lesson3":
                console.log("JS:You are in Lesson 3");
                return 3;
                // Additional actions specific to Lesson 3
            case "lesson4":
                console.log("JS:You are in Lesson 4");
                return 4;
                // Additional actions specific to Lesson 4
            case "lesson5":
                console.log("JS:You are in Lesson 5");
                return 5;
                // Additional actions specific to Lesson 5
            case "lesson6":
                console.log("JS:You are in Lesson 6");
                return 6;
                // Additional actions specific to Lesson 6
            default:
                console.log("Unknown lesson");
        }
    }

    //checkCurrentLesson(); //get rid of this

    function createObject(object, variableName) {
        globalThis[variableName] = object
    }

    //function that maps python object (left) to the global js variable
    // exports python functions to javascript
    //This way we can call python functions in JS
    //object is python object. VariableName is what you want it to be called in JS
    //called in pythonn
   // function createObject(object, variableName) {
       // globalThis[variableName] = object
    //}

    //JAV-CODE (above)


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
        this.textContent = isConnected ? 'Disconnect' : 'Connect Spike Prime';
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

    let is_running = false;
    // connect 'run python code' js button to mpy-editor
    runButton.addEventListener('click', function() {
        if (!is_running) {
            // run the code
            sensorButton.classList.remove('active');
            downloadButton.classList.remove('active');
            const editor = document.getElementById(this.getAttribute('data-editor-id'));
            if (editor) {
                const event = new CustomEvent('mpy-run', {
                    bubbles: true,
                    detail: { code: editor.code }
                });
                editor.dispatchEvent(event);
                this.innerHTML = 'Stop Running Code';
                is_running = true;
            }
        } else {
            // stop the code
            sensorButton.classList.add('active');
            downloadButton.classList.add('active');
            window.stop_running_code();
            this.innerHTML = 'Run Python Code';
            is_running = false;
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


    // Switch between the custom terminal and the debugger
    let customTerminal = document.getElementById('customTerminalButton');
    let defaultTerminal = document.getElementById('defaultTerminalButton');

    customTerminal.addEventListener("click", (event) => {
        changeTabTerminal(event, 'terminal');
    });

    defaultTerminal.addEventListener("click", (event) => {
        changeTabTerminal(event, 'debug');
    });
      
    function changeTabTerminal(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

    // fade the gifs in and out
    window.fadeImage = fadeImage;
    function fadeImage(newSrc) {
        const img = document.getElementById('gif');
        img.style.opacity = '0';
        setTimeout(() => {
            img.src = newSrc;
            img.style.opacity = '1';
        }, 500);
    }

    // make the custom terminal auto scroll on overflow
    window.scrollTerminalToBottom = function() {
        const terminal = document.getElementById('terminal');
        const messages = document.getElementById('terminalMessages');
        terminal.scrollTop = messages.scrollHeight;
    };

});