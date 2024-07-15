//  from ChatGPT

function readFile(file) {
    return new Promise((resolve, reject) => {
        if (file && file instanceof Blob) {
            const reader = new FileReader();

            reader.onload = (event) => {
                resolve(event.target.result);
            };

            reader.onerror = (error) => {
                reject(error);
            };

            reader.readAsText(file);
        } else {
            reject(new Error('No file selected or file is not of type Blob'));
        }
    });
}

async function saveFile(content, defaultFileName) {
        try {
            // Show file save dialog
            const handle = await window.showSaveFilePicker({
                suggestedName: defaultFileName,
                types: [{
                    description: 'Text Files',
                    accept: {'text/plain': ['.txt']},
                }],
            });
            const writableStream = await handle.createWritable();  // Create a writable stream
            await writableStream.write(content);           // Write the content to the file           
            await writableStream.close();                   // Close the file and write the contents to disk

            alert('File saved successfully!');
        } catch (error) {
            alert('Error saving file: ' + error.message);
        }
}

class Files {
    constructor() {
    this.file = null;
    this.callback = null;
    this.content = null;
    }

    read = async (name) => {
      try {
        const fileInput = document.getElementById(name);
        const file = fileInput.files[0];
        console.log(file)
        return await readFile(file);

        } catch (error) {
            console.log(`Error reading file: ${error.message}`);
        }
    };
    save = async (content, defaultname) => {
      try {
        await saveFile(content, defaultname);
        return true;

        } catch (error) {
            console.log(`Error saving file: ${error.message}`);
        }
    };
}

export function newFile() {
    return new Files();
}
