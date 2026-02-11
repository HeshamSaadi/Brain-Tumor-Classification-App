const fileInput = document.getElementById('file-input');
const previewWrapper = document.getElementById('preview-wrapper');
const previewImg = document.getElementById('image-preview');
const scanner = document.getElementById('scanner');
const uploadText = document.getElementById('upload-text');
const form = document.getElementById('main-form');
const resultArea = document.getElementById('result-area');
const submitBtn = document.getElementById('submit-btn');

fileInput.onchange = evt => {
    const [file] = fileInput.files;
    if (file) {
        previewImg.src = URL.createObjectURL(file);
        previewWrapper.style.display = 'block';
        uploadText.innerText = "File: " + file.name;
        resultArea.style.display = 'none';
    }
}

form.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    
    // Start Animations
    scanner.style.display = 'block';
    submitBtn.innerText = "Analyzing Structures...";
    submitBtn.disabled = true;
    resultArea.style.display = 'none';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        document.getElementById('prediction-text').innerText = data.prediction.toUpperCase();
        document.getElementById('confidence-text').innerText = "AI Confidence: " + data.confidence;
        resultArea.style.display = 'block';
    } catch (error) {
        alert("Analysis failed. Ensure the Flask server is active.");
    } finally {
        scanner.style.display = 'none';
        submitBtn.innerText = "Begin Analysis";
        submitBtn.disabled = false;
    }
};
