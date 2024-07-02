document.addEventListener('DOMContentLoaded', function() {
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
});