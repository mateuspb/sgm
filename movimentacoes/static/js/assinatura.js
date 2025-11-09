document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('signatureCanvas');
    const clearBtn = document.getElementById('clearSignature');
    const saveBtn = document.getElementById('saveSignature');
    const modalEl = document.getElementById('modalAssinatura');
    const inputMovId = document.getElementById('movimentacaoId');

    if (!canvas || !clearBtn || !saveBtn || !modalEl || !inputMovId) {
        console.error("Elementos não encontrados no DOM.");
        return;
    }

    let signaturePad = null;

    function ensurePad() {
        if (!signaturePad) signaturePad = new SignaturePad(canvas);
        resizeCanvas();
    }

    function resizeCanvas() {
        const container = canvas.parentElement;
        const width = (container?.clientWidth || 600);
        const height = (container?.clientHeight || 300);
        const ratio = Math.max(window.devicePixelRatio || 1, 1);

        canvas.width = Math.floor(width * ratio);
        canvas.height = Math.floor(height * ratio);
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';

        const ctx = canvas.getContext('2d');
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
        signaturePad && signaturePad.clear();
    }

    // === Integração correta com Bootstrap ===
    modalEl.addEventListener('shown.bs.modal', (e) => {
        // Botão que abriu o modal
        const opener = e.relatedTarget;
        if (opener) {
            inputMovId.value = opener.getAttribute('data-id') || '';
        }
        ensurePad(); // cria e ajusta o canvas quando o modal JÁ está visível
    });

    modalEl.addEventListener('hidden.bs.modal', () => {
        if (signaturePad) signaturePad.clear();
        inputMovId.value = '';
    });

    window.addEventListener('resize', () => {
        if (signaturePad) resizeCanvas();
    });

    clearBtn.addEventListener('click', () => {
        if (signaturePad) signaturePad.clear();
    });

    saveBtn.addEventListener('click', () => {
        if (!signaturePad) { alert('Campo de assinatura não inicializado.'); return; }
        if (signaturePad.isEmpty()) { alert('Faça a assinatura antes de salvar.'); return; }

        const assinatura = signaturePad.toDataURL();         // 'image/png'
        const dataAssinatura = new Date().toISOString();
        const movimentacaoId = inputMovId.value;

        if (!navigator.onLine) {
            const payload = JSON.stringify({ id: movimentacaoId, assinatura, dataAssinatura });
            localStorage.setItem(`assinatura-${movimentacaoId}`, payload);
            alert('Assinatura salva offline! Será sincronizada quando estiver online.');
            fecharModal();
        } else {
            salvarAssinaturaOnline(movimentacaoId, assinatura, dataAssinatura);
        }
    });

    function salvarAssinaturaOnline(id, assinatura, dataAssinatura, onOk) {
        fetch('/ajax/salvar-assinatura/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({ id, assinatura, dataAssinatura })
        })
            .then(res => res.ok ? res.json() : Promise.reject())
            .then(data => {
                alert((data && data.mensagem) || 'Assinatura sincronizada!');
                fecharModal();
                if (typeof onOk === 'function') onOk();
            })
            .catch(() => {
                const payload = JSON.stringify({ id, assinatura, dataAssinatura });
                localStorage.setItem(`assinatura-${id}`, payload);
                alert('Sem conexão estável. Assinatura salva offline.');
                fecharModal();
            });
    }

    function fecharModal() {
        const instance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        instance.hide(); // fecha do jeito certo no Bootstrap
        // reload opcional se você quiser atualizar a tabela:
        location.reload();
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Sincroniza offline -> online
    window.addEventListener('online', () => {
        Object.keys(localStorage).forEach((key) => {
            if (!key.startsWith('assinatura-')) return;
            try {
                const { id, assinatura, dataAssinatura } = JSON.parse(localStorage.getItem(key) || '{}');
                if (id && assinatura) {
                    salvarAssinaturaOnline(id, assinatura, dataAssinatura, () => {
                        localStorage.removeItem(key);
                    });
                }
            } catch (_) { }
        });
    });
});