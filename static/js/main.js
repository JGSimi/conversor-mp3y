document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('converter-form');
    const urlInput = document.getElementById('url-input');
    const convertBtn = document.getElementById('convert-btn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');

    const API_BASE_URL = 'http://127.0.0.1:5001';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) {
            showError('Por favor, insira uma URL do YouTube');
            return;
        }

        try {
            // Resetar estado
            hideError();
            showLoading();
            disableForm();

            // Fazer requisição para o backend
            const response = await fetch(`${API_BASE_URL}/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ url }),
                mode: 'cors',
                credentials: 'omit'
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || `Erro ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            showResult(data);
        } catch (err) {
            console.error('Erro:', err);
            showError(err.message || 'Erro ao processar sua solicitação. Tente novamente.');
        } finally {
            hideLoading();
            enableForm();
        }
    });

    function showLoading() {
        loading.style.display = 'block';
        result.style.display = 'none';
    }

    function hideLoading() {
        loading.style.display = 'none';
    }

    function showResult(data) {
        result.innerHTML = `
            <h3>${data.title}</h3>
            <button onclick="window.location.href='${API_BASE_URL}/download/${data.filename}'" class="download-btn">
                <i class="fas fa-download"></i> Baixar MP3
            </button>
        `;
        result.style.display = 'block';
    }

    function showError(message) {
        error.textContent = message;
        error.style.display = 'block';
        result.style.display = 'none';
    }

    function hideError() {
        error.style.display = 'none';
    }

    function disableForm() {
        urlInput.disabled = true;
        convertBtn.disabled = true;
    }

    function enableForm() {
        urlInput.disabled = false;
        convertBtn.disabled = false;
    }
}); 