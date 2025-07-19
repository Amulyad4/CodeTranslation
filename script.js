document.addEventListener('DOMContentLoaded', function() {
    const translateBtn = document.getElementById('translateBtn');
    const clearSourceBtn = document.getElementById('clearSource');
    const copyOutputBtn = document.getElementById('copyOutput');
    const swapLangsBtn = document.getElementById('swapLangs');
    const sourceCode = document.getElementById('sourceCode');
    const translatedCode = document.getElementById('translatedCode');
    const sourceLang = document.getElementById('sourceLang');
    const targetLang = document.getElementById('targetLang');
    
    const API_PORT = 5001;
    const API_URL = `http://localhost:${API_PORT}/translate`;
    
    // Set default languages that are different
    if (sourceLang.value === targetLang.value) {
        targetLang.value = 'javascript';
    }
    
    translateBtn.addEventListener('click', translateCode);
    clearSourceBtn.addEventListener('click', () => sourceCode.value = '');
    copyOutputBtn.addEventListener('click', copyTranslatedCode);
    swapLangsBtn.addEventListener('click', swapLanguages);
    
    async function translateCode() {
        const code = sourceCode.value.trim();
        if (!code) {
            showAlert('Please enter some code to translate', 'warning');
            return;
        }
        
        if (sourceLang.value === targetLang.value) {
            showAlert('Source and target languages must be different', 'warning');
            return;
        }
        
        translateBtn.disabled = true;
        translateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Translating...';
        
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: code,
                    source_lang: sourceLang.value,
                    target_lang: targetLang.value,
                    method: 'ast' // Using only AST now
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                translatedCode.value = data.translated_code;
                showAlert('Translation successful!', 'success');
            } else {
                throw new Error(data.error || 'Translation failed');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert(`Error: ${error.message}`, 'danger');
            translatedCode.value = '';
        } finally {
            translateBtn.disabled = false;
            translateBtn.innerHTML = '<i class="fas fa-exchange-alt me-2"></i> Translate Code';
        }
    }
    
    function copyTranslatedCode() {
        if (!translatedCode.value) {
            showAlert('No translated code to copy', 'warning');
            return;
        }
        
        translatedCode.select();
        document.execCommand('copy');
        
        // Visual feedback
        const originalText = copyOutputBtn.innerHTML;
        copyOutputBtn.innerHTML = '<i class="fas fa-check me-1"></i> Copied!';
        setTimeout(() => {
            copyOutputBtn.innerHTML = originalText;
        }, 2000);
    }
    
    function swapLanguages() {
        const temp = sourceLang.value;
        sourceLang.value = targetLang.value;
        targetLang.value = temp;
        
        // Swap code if there's already a translation
        if (translatedCode.value) {
            const tempCode = sourceCode.value;
            sourceCode.value = translatedCode.value;
            translatedCode.value = tempCode;
        }
    }
    
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.maxWidth = '300px';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 3000);
    }
});
// Add to your existing script.js
document.getElementById('downloadOutput').addEventListener('click', downloadAsPDF);

async function downloadAsPDF() {
    if (!translatedCode.value) {
        showAlert('No translated code to download', 'warning');
        return;
    }

    // Create a new PDF instance
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(18);
    doc.setTextColor(58, 65, 111);
    doc.text('Code Translation Result', 105, 20, { align: 'center' });
    
    // Add metadata
    doc.setFontSize(12);
    doc.setTextColor(100, 100, 100);
    doc.text(`From: ${sourceLang.options[sourceLang.selectedIndex].text}`, 20, 35);
    doc.text(`To: ${targetLang.options[targetLang.selectedIndex].text}`, 20, 45);
    doc.text(new Date().toLocaleString(), 20, 55);
    
    // Add the translated code
    doc.setFontSize(11);
    doc.setTextColor(0, 0, 0);
    doc.setFont('courier', 'normal');
    
    // Split long lines and handle overflow
    const lines = doc.splitTextToSize(translatedCode.value, 180);
    doc.text(lines, 20, 70);
    
    // Save the PDF
    doc.save('translated_code.pdf');
    showAlert('PDF downloaded successfully!', 'success');
}