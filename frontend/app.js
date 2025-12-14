// API base URL - automatically detects subdirectory
const API_BASE = window.location.origin + (window.location.pathname.includes('/pem08') ? '/pem08' : '');

// Global variables
let currentImageFile = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initImageUpload();
    loadHistory();
});

// === TAB NAVIGATION ===
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to selected tab
            button.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// === IMAGE UPLOAD ===
function initImageUpload() {
    const uploadArea = document.getElementById('upload-area');
    const imageInput = document.getElementById('image-input');
    
    // Click on upload area
    uploadArea.addEventListener('click', () => {
        imageInput.click();
    });
    
    // File selection
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageFile(file);
        }
    });
    
    // Drag & Drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageFile(file);
        } else {
            showStatus('Please upload an image', 'error');
        }
    });
}

function handleImageFile(file) {
    currentImageFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('preview-img').src = e.target.result;
        document.getElementById('image-name').textContent = file.name;
        document.querySelector('.upload-placeholder').style.display = 'none';
        document.getElementById('image-preview').style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    currentImageFile = null;
    document.getElementById('image-input').value = '';
    document.querySelector('.upload-placeholder').style.display = 'block';
    document.getElementById('image-preview').style.display = 'none';
}

// === TEXT ANALYSIS ===
async function analyzeText() {
    const text = document.getElementById('text-input').value.trim();
    const competitorName = document.getElementById('competitor-name').value.trim();
    
    if (!text) {
        showStatus('Enter text to analyze', 'error');
        return;
    }
    
    showStatus('Analyzing text...', 'info');
    
    try {
        const response = await fetch(`${API_BASE}/analyze_text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                competitor_name: competitorName || null
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTextAnalysis(data.analysis);
            showStatus('Analysis complete!', 'success');
        } else {
            throw new Error(data.detail || 'Analysis error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error(error);
    }
}

function displayTextAnalysis(analysis) {
    const resultBox = document.getElementById('text-result');
    const resultContent = document.getElementById('text-result-content');
    
    let html = '';
    
    // Scores
    if (analysis.design_score !== undefined) {
        html += `
            <div class="score-grid">
                <div class="score-item">
                    <span class="score-value">${analysis.design_score}/10</span>
                    <span class="score-label">Design</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${analysis.animation_potential}/10</span>
                    <span class="score-label">Animation</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${analysis.innovation_score}/10</span>
                    <span class="score-label">Innovation</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${analysis.technical_execution}/10</span>
                    <span class="score-label">Execution</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${analysis.client_focus}/10</span>
                    <span class="score-label">Clients</span>
                </div>
            </div>
        `;
    }
    
    // Strengths
    if (analysis.strengths && analysis.strengths.length > 0) {
        html += `
            <div class="analysis-section">
                <h4>✅ Strengths:</h4>
                <ul>
                    ${analysis.strengths.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Weaknesses
    if (analysis.weaknesses && analysis.weaknesses.length > 0) {
        html += `
            <div class="analysis-section">
                <h4>⚠️ Weaknesses:</h4>
                <ul>
                    ${analysis.weaknesses.map(w => `<li class="weakness">${w}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Style analysis
    if (analysis.style_analysis) {
        html += `
            <div class="analysis-section">
                <h4>🎨 Style Analysis:</h4>
                <p>${analysis.style_analysis}</p>
            </div>
        `;
    }
    
    // Recommendations
    if (analysis.improvement_recommendations && analysis.improvement_recommendations.length > 0) {
        html += `
            <div class="analysis-section">
                <h4>💡 Recommendations:</h4>
                <ul>
                    ${analysis.improvement_recommendations.map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Summary
    if (analysis.summary) {
        html += `
            <div class="analysis-section">
                <h4>📊 Summary:</h4>
                <p>${analysis.summary}</p>
            </div>
        `;
    }
    
    resultContent.innerHTML = html;
    resultBox.style.display = 'block';
}

// === IMAGE ANALYSIS ===
async function analyzeImage() {
    if (!currentImageFile) {
        showStatus('Select an image to analyze', 'error');
        return;
    }
    
    showStatus('Analyzing image...', 'info');
    
    try {
        const formData = new FormData();
        formData.append('file', currentImageFile);
        
        const response = await fetch(`${API_BASE}/analyze_image`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayImageAnalysis(data.analysis);
            showStatus('Analysis complete!', 'success');
        } else {
            throw new Error(data.detail || 'Analysis error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error(error);
    }
}

function displayImageAnalysis(analysis) {
    const resultBox = document.getElementById('image-result');
    const resultContent = document.getElementById('image-result-content');
    
    let html = `
        <div class="analysis-section">
            <h4>📝 Description:</h4>
            <p>${analysis.description || 'No description'}</p>
        </div>
    `;
    
    if (analysis.design_score !== undefined) {
        html += `
            <div class="score-grid">
                <div class="score-item">
                    <span class="score-value">${analysis.design_score}/10</span>
                    <span class="score-label">Design</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${analysis.animation_potential}/10</span>
                    <span class="score-label">Animation</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${analysis.visual_style_score}/10</span>
                    <span class="score-label">Visual</span>
                </div>
            </div>
        `;
    }
    
    if (analysis.visual_style_analysis) {
        html += `
            <div class="analysis-section">
                <h4>🎨 Visual style:</h4>
                <p>${analysis.visual_style_analysis}</p>
            </div>
        `;
    }
    
    if (analysis.recommendations && analysis.recommendations.length > 0) {
        html += `
            <div class="analysis-section">
                <h4>💡 Recommendations:</h4>
                <ul>
                    ${analysis.recommendations.map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    resultContent.innerHTML = html;
    resultBox.style.display = 'block';
}

// === SITE PARSING ===
async function parseWebsite() {
    const url = document.getElementById('url-input').value.trim();
    
    if (!url) {
        showStatus('Enter site URL', 'error');
        return;
    }
    
    showProgress(true);
    showStatus('Parsing site...', 'info');
    
    try {
        const response = await fetch(`${API_BASE}/parse_demo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayParseResults(data);
            showStatus('Parsing complete!', 'success');
        } else {
            throw new Error(data.error || 'Parsing error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showProgress(false);
    }
}

function displayParseResults(data) {
    const resultBox = document.getElementById('parse-result');
    const resultContent = document.getElementById('parse-result-content');
    
    let html = `
        <div class="analysis-section">
            <h4>🌐 URL:</h4>
            <p><a href="${data.url}" target="_blank">${data.url}</a></p>
        </div>
    `;
    
    if (data.text_preview) {
        html += `
            <div class="analysis-section">
                <h4>📄 Content preview:</h4>
                <p>${data.text_preview}</p>
            </div>
        `;
    }
    
    if (data.analysis) {
        html += '<div class="analysis-section"><h4>📊 AI analysis:</h4></div>';
        
        // Use text analysis display function
        const tempDiv = document.createElement('div');
        document.body.appendChild(tempDiv);
        const oldContent = document.getElementById('text-result-content');
        const tempContent = document.createElement('div');
        tempContent.id = 'text-result-content';
        tempDiv.appendChild(tempContent);
        
        displayTextAnalysis(data.analysis);
        html += tempContent.innerHTML;
        
        document.body.removeChild(tempDiv);
    }
    
    resultContent.innerHTML = html;
    resultBox.style.display = 'block';
}

async function parseAllCompetitors() {
    showProgress(true);
    showStatus('Starting bulk parsing...', 'info');
    
    try {
        const response = await fetch(`${API_BASE}/parse_all`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`Successfully analyzed ${data.total} competitors!`, 'success');
            
            const resultBox = document.getElementById('parse-result');
            const resultContent = document.getElementById('parse-result-content');
            
            resultContent.innerHTML = `
                <div class="analysis-section">
                    <h4>✅ Bulk parsing complete</h4>
                    <p>Total analyzed: <strong>${data.total}</strong> competitors</p>
                    <p>Results saved to file: <code>data/parsing_results.json</code></p>
                </div>
            `;
            
            resultBox.style.display = 'block';
        } else {
            throw new Error('Bulk parsing error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showProgress(false);
    }
}

function showProgress(show) {
    const progressBar = document.getElementById('parse-progress');
    progressBar.style.display = show ? 'block' : 'none';
}

// === HISTORY ===
async function loadHistory() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '<p class="loading"><span class="spinner"></span> Loading history...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/history`);
        const data = await response.json();
        
        if (data.items && data.items.length > 0) {
            let html = '';
            
            data.items.forEach(item => {
                const date = new Date(item.timestamp);
                const formattedDate = date.toLocaleString('en-US');
                
                html += `
                    <div class="history-item">
                        <div class="history-item-header">
                            <span class="history-type">${getRequestTypeLabel(item.request_type)}</span>
                            <span class="history-time">${formattedDate}</span>
                        </div>
                        <div class="history-content">
                            <p><strong>Request:</strong> ${item.request_summary}</p>
                            <p><strong>Result:</strong> ${item.response_summary}</p>
                        </div>
                    </div>
                `;
            });
            
            historyList.innerHTML = html;
        } else {
            historyList.innerHTML = '<p class="loading">History is empty</p>';
        }
    } catch (error) {
        historyList.innerHTML = '<p class="loading">Error loading history</p>';
        console.error(error);
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear all history?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/history`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus('History cleared', 'success');
            loadHistory();
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error(error);
    }
}

function getRequestTypeLabel(type) {
    const labels = {
        'text_analysis': '📝 Text analysis',
        'image_analysis': '🖼️ Image analysis',
        'parsing': '🌐 Site parsing'
    };
    return labels[type] || type;
}

// === EXAMPLES ===
function loadExampleText() {
    // Text split into parts for convenience
    const lines = [
        '\u0421\u0442\u0443\u0434\u0438\u044f MotionCraft \u2014 \u043b\u0438\u0434\u0435\u0440 \u0432 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0438 3D-\u0430\u043d\u0438\u043c\u0430\u0446\u0438\u0438 \u0438 \u043c\u043e\u0443\u0448\u043d-\u0434\u0438\u0437\u0430\u0439\u043d\u0430 \u0434\u043b\u044f \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0439.',
        '',
        '\u041d\u0430\u0448\u0438 \u043a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0443\u0441\u043b\u0443\u0433\u0438:',
        '\u2022 \u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0430\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0440\u043e\u043b\u0438\u043a\u043e\u0432 \u0434\u043b\u044f \u043f\u0440\u0435\u0437\u0435\u043d\u0442\u0430\u0446\u0438\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432',
        '\u2022 \u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430 3D-\u0432\u0438\u0437\u0443\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0439 \u0434\u043b\u044f SaaS-\u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c',
        '\u2022 \u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u043e \u0440\u0435\u043a\u043b\u0430\u043c\u043d\u044b\u0445 \u0440\u043e\u043b\u0438\u043a\u043e\u0432 \u0434\u043b\u044f IT-\u0441\u0442\u0430\u0440\u0442\u0430\u043f\u043e\u0432',
        '\u2022 \u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0430\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0438\u043d\u0444\u043e\u0433\u0440\u0430\u0444\u0438\u043a',
        '',
        '\u0422\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u0442\u0435\u043a:',
        '- Cinema 4D + Redshift',
        '- After Effects + Lottie',
        '- Blender \u0434\u043b\u044f 3D-\u043c\u043e\u0434\u0435\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f',
        '- Figma \u0434\u043b\u044f \u043f\u0440\u0435-\u043f\u0440\u043e\u0434\u0430\u043a\u0448\u043d',
        '',
        '\u041d\u0430\u0448 \u043f\u043e\u0434\u0445\u043e\u0434: \u0433\u043b\u0443\u0431\u043e\u043a\u043e\u0435 \u043f\u043e\u0433\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u0432 \u043f\u0440\u043e\u0434\u0443\u043a\u0442 \u043a\u043b\u0438\u0435\u043d\u0442\u0430, agile-\u043c\u0435\u0442\u043e\u0434\u043e\u043b\u043e\u0433\u0438\u044f \u0440\u0430\u0431\u043e\u0442\u044b,',
        '\u0444\u043e\u043a\u0443\u0441 \u043d\u0430 \u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0435 \u0441\u043b\u043e\u0436\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043a\u043e\u043d\u0446\u0435\u043f\u0446\u0438\u0439 \u0447\u0435\u0440\u0435\u0437 \u043f\u0440\u043e\u0441\u0442\u0443\u044e \u0438 \u043a\u0440\u0430\u0441\u0438\u0432\u0443\u044e \u0430\u043d\u0438\u043c\u0430\u0446\u0438\u044e.',
        '',
        '\u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e \u0432\u043a\u043b\u044e\u0447\u0430\u0435\u0442 \u043f\u0440\u043e\u0435\u043a\u0442\u044b \u0434\u043b\u044f Yandex, Tinkoff, VK \u0438 \u0434\u0440\u0443\u0433\u0438\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0433\u0438\u0433\u0430\u043d\u0442\u043e\u0432.'
    ];
    
    const exampleText = lines.join('\n');
    
    document.getElementById('text-input').value = exampleText;
    document.getElementById('competitor-name').value = 'MotionCraft Studio';
    showStatus('Example loaded', 'info');
}

// === UTILITIES ===
function showStatus(message, type = 'info') {
    const statusBar = document.getElementById('status-bar');
    const statusMessage = document.getElementById('status-message');
    
    statusBar.className = 'status-bar';
    if (type === 'error') {
        statusBar.classList.add('error');
    } else if (type === 'info') {
        statusBar.classList.add('info');
    }
    
    statusMessage.textContent = message;
    statusBar.style.display = 'block';
    
    setTimeout(() => {
        statusBar.style.display = 'none';
    }, 5000);
}
