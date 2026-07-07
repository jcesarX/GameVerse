//Remoção da Mensagem de Erro
document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");

    flashes.forEach((flash) => {
        setTimeout(() => {
            flash.classList.add("fade-out");

            setTimeout(() => {
                flash.remove();
            }, 500);
        }, 5000);
    });
});

//Responsividade da Paginação
(function() {
    function larguraParaJogosPorPagina() {
        const largura = window.innerWidth;
        if (largura >= 1200) return 8;   //Monitor grande
        if (largura >= 992)  return 6;   //Notebook
        if (largura >= 600)  return 4;   //Tablet
        return 2;                        //Celular
    }

    function getCookie(nome) {
        const match = document.cookie.match(new RegExp('(^| )' + nome + '=([^;]+)'));
        return match ? match[2] : null;
    }

    const valorIdeal = larguraParaJogosPorPagina();
    const valorAtual = getCookie('jogos_por_pagina');

    if (String(valorIdeal) !== valorAtual) {
        document.cookie = 'jogos_por_pagina=' + valorIdeal + ';path=/;max-age=31536000';
        window.location.reload();
    }
})();