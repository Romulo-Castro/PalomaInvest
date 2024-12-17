const urlParams = new URLSearchParams(window.location.search);
const codigo = urlParams.get('codigo');
document.addEventListener("DOMContentLoaded", function () {
    // const urlParams = new URLSearchParams(window.location.search);
    // const codigo = urlParams.get('codigo');

    if (codigo) {
        console.log("Código da ação:", codigo);
        fetchStockDetails(codigo);
    } else {
        console.error("Código da ação não encontrado na URL.");
        displayError("Código da ação não encontrado.");
    }
});

function voltar() {
    window.location.href = "/app/view/home/index.html";
}

function gerarTese() {
    // Armazena o código da ação no localStorage
    localStorage.setItem('codigo', codigo);

    // Redireciona para a tela de tese
    window.location.href = '/app/view/tese/tese.html';
}

function fetchStockDetails(codigo) {
    const apiUrl = `http://127.0.0.1:5000/acoes/detalhes?codigo=${codigo}`;

    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Erro ao carregar os detalhes da ação");
            }
            return response.json();
        })
        .then((stockDetails) => {
            console.log("Detalhes da ação recebidos:", stockDetails);
            displayStockDetails(stockDetails);
        })
        .catch((error) => {
            console.error(error.message);
            displayError(error.message);
        });
}

function displayStockDetails(stockDetails) {
    const stock = Array.isArray(stockDetails) ? stockDetails[0] : stockDetails;

    if (!stock) {
        displayError("Detalhes da ação não encontrados.");
        return;
    }

    // Preenche os campos com os dados
    document.getElementById('codigo').innerText = stock.codigo || "-";
    document.getElementById("nome_empresa").innerText = stock.nome_empresa || "-";
    document.getElementById("setor").innerText = stock.setor || "-";
    document.getElementById("tipo").innerText = stock.tipo || "-";
    document.getElementById("cotacao").innerText = stock.cotacao || "-";
    document.getElementById("div_yield").innerText = stock.div_yield || "-";
    document.getElementById("pl").innerText = stock.pl || "-";
    document.getElementById("pvp").innerText = stock.pvp || "-";
    document.getElementById("vpa").innerText = stock.vpa || "-";
    document.getElementById("lpa").innerText = stock.lpa || "-";
    document.getElementById("roe").innerText = stock.roe || "-";
    document.getElementById("patrim_liq").innerText = stock.patrim_liq || "-";
    document.getElementById("valor_mercado").innerText = stock.valor_mercado || "-";
    document.getElementById("data_ultima_cotacao").innerText = stock.data_ultima_cotacao || "-";
    document.getElementById("receita_liquida_12m").innerText = stock.receita_liquida_12m || "-";
    document.getElementById("divida_liquida").innerText = stock.divida_liquida || "-";
    document.getElementById("lucro_liquido_12m").innerText = stock.lucro_liquido_12m || "-";
    document.getElementById("max_52_sem").innerText = stock.max_52_sem || "-";
    document.getElementById("min_52_sem").innerText = stock.min_52_sem || "-";
    document.getElementById("ebit_12m").innerText = stock.ebit_12m || "-";
}

function displayError(message) {
    alert(message);
}
