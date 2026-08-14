// Remoção automática das mensagens de erro/flash
function iniciarFadeDosFlashes(raiz) {
    const flashes = (raiz || document).querySelectorAll(".flash, .form-erro");

    flashes.forEach((flash) => {
        setTimeout(() => {
            flash.classList.add("fade-out");
            setTimeout(() => flash.remove(), 500);
        }, 5000);
    });
}

document.addEventListener("DOMContentLoaded", () => iniciarFadeDosFlashes());

// Responsividade da paginação: ajusta quantos jogos são exibidos
// por página de acordo com a largura da tela (via cookie lido no backend)
(function () {
    function larguraParaJogosPorPagina() {
        const largura = window.innerWidth;
        if (largura >= 1200) return 12;  // Monitor grande
        if (largura >= 992) return 8;    // Notebook
        if (largura >= 600) return 6;    // Tablet
        return 6;                        // Celular
    }

    function getCookie(nome) {
        const match = document.cookie.match(new RegExp("(^| )" + nome + "=([^;]+)"));
        return match ? match[2] : null;
    }

    const valorIdeal = larguraParaJogosPorPagina();
    const valorAtual = getCookie("jogos_por_pagina");

    if (String(valorIdeal) !== valorAtual) {
        document.cookie = "jogos_por_pagina=" + valorIdeal + ";path=/;max-age=31536000";
        if (valorAtual !== null) {
            window.location.reload();
        }
    }
})();

// Painéis laterais (filtros e formulário de cadastro/edição)
(function () {
    const overlay = document.getElementById("overlay-painel");
    const sidebarFiltros = document.getElementById("sidebar-filtros");
    const btnAbrirFiltros = document.getElementById("abrir-filtros");
    const painelFormulario = document.getElementById("painel-formulario");

    function fecharTudo() {
        if (sidebarFiltros) sidebarFiltros.classList.remove("aberta");
        if (painelFormulario) painelFormulario.classList.remove("aberta");
        if (overlay) overlay.classList.remove("visivel");
    }

    function abrirFiltros() {
        if (!sidebarFiltros) return;
        if (painelFormulario) painelFormulario.classList.remove("aberta");
        sidebarFiltros.classList.add("aberta");
        overlay.classList.add("visivel");
    }

    function abrirPainelFormulario(html) {
        if (!painelFormulario) return;
        if (sidebarFiltros) sidebarFiltros.classList.remove("aberta");
        painelFormulario.innerHTML = html;
        painelFormulario.classList.add("aberta");
        overlay.classList.add("visivel");
        iniciarFadeDosFlashes(painelFormulario);
    }

    function fecharPainelFormulario() {
        if (!painelFormulario) return;
        painelFormulario.classList.remove("aberta");
        overlay.classList.remove("visivel");
    }

    function atualizarGrade() {
        const grade = document.getElementById("grade-resultados");
        if (!grade) return;
        fetch(window.location.href, { headers: { "X-Requested-With": "fetch" } })
            .then((resposta) => resposta.text())
            .then((html) => {
                document.getElementById("grade-resultados").outerHTML = html;
            });
    }

    if (btnAbrirFiltros) {
        btnAbrirFiltros.addEventListener("click", abrirFiltros);
    }

    if (overlay) {
        overlay.addEventListener("click", fecharTudo);
    }

    document.getElementById("fechar-filtros")?.addEventListener("click", fecharTudo);

    // Abre o painel de cadastro/edição (delegação: os botões podem
    // existir em páginas diferentes, como o index e a página do jogo)
    document.addEventListener("click", (evento) => {
        const botaoAbrir = evento.target.closest(".abrir-painel-formulario");
        if (botaoAbrir) {
            const url = botaoAbrir.dataset.url;
            fetch(url, { headers: { "X-Requested-With": "fetch" } })
                .then((resposta) => resposta.text())
                .then((html) => abrirPainelFormulario(html));
            return;
        }

        const botaoFechar = evento.target.closest(".fechar-painel-formulario");
        if (botaoFechar) {
            if (botaoFechar.closest("#painel-formulario")) {
                fecharPainelFormulario();
            } else {
                // Página de fallback (sem JS/navegação direta): volta pro catálogo
                window.location.href = "/";
            }
        }
    });

    // Envio do formulário de cadastro/edição dentro do painel
    document.addEventListener("submit", (evento) => {
        const form = evento.target.closest(".form-jogo");
        if (!form || !form.closest("#painel-formulario")) return;

        evento.preventDefault();

        const dadosForm = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: dadosForm,
            headers: { "X-Requested-With": "fetch" }
        }).then((resposta) => {
            if (resposta.ok) {
                fecharPainelFormulario();
                if (document.getElementById("grade-resultados")) {
                    atualizarGrade();
                } else {
                    window.location.reload();
                }
                return;
            }

            resposta.text().then((html) => abrirPainelFormulario(html));
        });
    });
})();
