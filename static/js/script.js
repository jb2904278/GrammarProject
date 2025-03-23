document.getElementById("grammarForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const inputText = document.getElementById("inputText").value;

    // Show the original sentence
    document.getElementById("originalText").textContent = `Original: ${inputText}`;

    const response = await fetch("/correct", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
    });

    const data = await response.json();
    
    // Display the corrected sentence
    document.getElementById("correctedText").textContent = data.corrected_text;
});
