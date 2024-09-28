document.addEventListener('DOMContentLoaded', function() {
    // Handle the summarization form submission
    document.getElementById('textForm')?.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevents the default form submission

        const inputText = document.getElementById('inputBox').value;
        const summaryLine = document.getElementById('summary_line').value;

        // Send data to the Flask backend
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ inputText: inputText, summaryLine: summaryLine }),
        });

        const data = await response.json();

        // Display the output in the output box
        document.getElementById('outputBox').value = data.summaryText;
    });

    // Handle the translation form submission
    document.getElementById('translationForm')?.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevents the default form submission

        const inputText2 = document.getElementById('inputBox2').value;

        // Send data to the Flask backend
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ inputText2: inputText2 }),
        });

        const data = await response.json();

        // Display the output in the translated text box
        document.getElementById('translatedText').value = data.translatedText;
    });

    // Function to update word count
    function updateWordCount(textarea, countElement) {
        const text = textarea.value.trim();
        const words = text ? text.split(/\s+/) : [];
        countElement.textContent = `${words.length} words`;
    }

    // Update word count as the user types
    const inputTextarea = document.getElementById('inputBox');
    const inputWordCount = document.getElementById('input-word-count');
    const outputTextarea = document.getElementById('outputBox');
    const outputWordCount = document.getElementById('output-word-count');
    const inputTextarea2 = document.getElementById('inputBox2');
    const inputWordCount2 = document.getElementById('input-word-count2');
    const translatedTextarea = document.getElementById('translatedText');
    const translatedWordCount = document.getElementById('translated-word-count');

    if (inputTextarea) updateWordCount(inputTextarea, inputWordCount);
    if (outputTextarea) updateWordCount(outputTextarea, outputWordCount);
    if (inputTextarea2) updateWordCount(inputTextarea2, inputWordCount2);
    if (translatedTextarea) updateWordCount(translatedTextarea, translatedWordCount);

    // Add event listeners for updating word counts
    if (inputTextarea) inputTextarea.addEventListener('input', function() {
        updateWordCount(inputTextarea, inputWordCount);
    });
    if (inputTextarea2) inputTextarea2.addEventListener('input', function() {
        updateWordCount(inputTextarea2, inputWordCount2);
    });
});
