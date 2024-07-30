/**
 * @file script.js
 * @description Main script for handling various UI interactions and 
 * functionality for the Spike Prime AI Puppy project.
 * @authors 
 *  - William Goldman
 *  - Javier Laveaga
 * @version 1.0
 */


document.addEventListener('DOMContentLoaded', function() {
    const connectButton = document.getElementById('connect-spike');
    const downloadButton = document.getElementById('download-code');
    const sensorButton = document.getElementById('sensor_readings');
    
    window.checkCurrentLesson = checkCurrentLesson;
    /**
     * @function checkCurrentLesson
     * @description Determines the current lesson based on the body ID and 
     * performs actions accordingly.
     * @returns {number} The lesson number.
     */
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

    // Code for resizable terminal
    let topBox = document.querySelector('.right-box:first-child');
    let bottomBox = document.getElementById("resizeBox");
    let slider = document.querySelector(".slider");
    let container = document.querySelector('.right-container');

    let startY;
    let startTopHeight;
    let startBottomHeight;

    slider.addEventListener('mousedown', initDrag, false);

    /**
     * @function initDrag
     * @description Initializes the drag event for resizing terminal boxes.
     * @param {MouseEvent} e - The mousedown event.
     */
    function initDrag(e) {
        startY = e.clientY;
        startTopHeight = topBox.offsetHeight;
        startBottomHeight = bottomBox.offsetHeight;
        
        document.documentElement.addEventListener('mousemove', doDrag, false);
        document.documentElement.addEventListener('mouseup', stopDrag, false);
    }

    /**
     * @function doDrag
     * @description Handles the dragging for resizing terminal boxes.
     * @param {MouseEvent} e - The mousemove event.
     */
    function doDrag(e) {
        let newTopHeight = startTopHeight + e.clientY - startY;
        let newBottomHeight = startBottomHeight - (e.clientY - startY);

        if (newTopHeight > 50 && newBottomHeight > 50) {
            topBox.style.height = newTopHeight + 'px';
            bottomBox.style.height = newBottomHeight + 'px';
        }
    }

    /**
     * @function stopDrag
     * @description Stops the dragging event for resizing terminal boxes.
     */
    function stopDrag() {
        document.documentElement.removeEventListener('mousemove', doDrag, false);
        document.documentElement.removeEventListener('mouseup', stopDrag, false);
    }


    // Switch between the custom terminal and the debugger
    let customTerminal = document.getElementById('customTerminalButton');
    let defaultTerminal = document.getElementById('defaultTerminalButton');
    
    customTerminal.addEventListener("click", (event) => {
        window.not_debugging() //calling python function
        changeTabTerminal(event, 'terminal');
    });

    //This one is the Debug terminal
    defaultTerminal.addEventListener("click", (event) => {
        console.log('IN DEBUG')
        window.debugging_time(); //calling python function
        changeTabTerminal(event, 'debug');
        //call python funciton which disables custom terminal button
    });
      
    /**
     * @function changeTabTerminal
     * @description Changes the displayed terminal tab.
     * @param {Event} evt - The click event.
     * @param {string} tabName - The name of the tab to display.
     */
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
    /**
     * @function fadeImage
     * @description Fades an image in and out.
     * @param {string} newSrc - The new source of the image.
     */
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

    /*FOR HITTING RUN BUTON*/ 
    //const buttons = document.querySelectorAll(".button--toggle");
    const nice_jav_button = document.querySelector("#custom-run-button");
    let is_running = false;
    nice_jav_button.addEventListener("click", function () {
    nice_jav_button.classList.toggle("is-active");
    if (!is_running) {
        // run the code
        const editor = document.getElementById(this.getAttribute('data-editor-id'));
        if (editor) {
            const event = new CustomEvent('mpy-run', {
                bubbles: true,
                detail: { code: editor.code }
            });
            editor.dispatchEvent(event);
            is_running = true;
        }
    } else {
        // stop the code
        window.stop_running_code(); //calling python function
        is_running = false;
    }
    });

    //programmatically click the hidden upload file input 
    //element after clicking the Upload button
    document.getElementById('chooseFileButton').addEventListener('click', function() {
        document.getElementById('fileRead').click();
    });
    
    //For fading in image of the warning sign exclamtionm mark
    window.startFadingWarningIcon = startFadingWarningIcon;
    let fadeInterval;
    /**
     * @function startFadingWarningIcon
     * @description Starts the fading animation for the warning icon.
     */
    function startFadingWarningIcon() {
        const downloadButton = document.getElementById('download-code');

        fadeInterval = setInterval(() => {
            if (downloadButton.classList.contains('fade-in')) {
                downloadButton.classList.remove('fade-in');
                downloadButton.classList.add('fade-out');
            } else {
                downloadButton.classList.remove('fade-out');
                downloadButton.classList.add('fade-in');
            }
        }, 500); // Adjust interval time as needed
    }
    
    window.stopFadingWarningIcon = stopFadingWarningIcon;
    /**
     * @function stopFadingWarningIcon
     * @description Stops the fading animation for the warning icon.
     */
    function stopFadingWarningIcon() {
        clearInterval(fadeInterval);
        const downloadButton = document.getElementById('download-code');
        downloadButton.classList.remove('fade-in', 'fade-out');
    }
});