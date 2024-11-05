document.addEventListener("DOMContentLoaded", function() {
    // Captura o parâmetro 'codigo' da URL
    const urlParams = new URLSearchParams(window.location.search);
    const codigo = urlParams.get('codigo');
    
    if (codigo) {
        // Exibe o código para verificar
        console.log("Código da ação:", codigo);

        // Chama a função para buscar detalhes da ação usando o código
        fetchStockDetails(codigo);
    } else {
        console.error("Código da ação não encontrado na URL.");
    }
});

// Função para buscar os detalhes da ação usando o código
function fetchStockDetails(codigo) {
    const apiUrl = `http://127.0.0.1:5000/acoes/detalhes?codigo=${codigo}`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar os detalhes da ação');
            }
            return response.json();
        })
        .then(stockDetails => {
            console.log("Detalhes da ação:", stockDetails);
            displayStockDetails(stockDetails);
        })
        .catch(error => {
            console.error(error.message);
            document.getElementById('stock-details').innerText = error.message;
        });
}

// Função para exibir os detalhes da ação na página
// Função para exibir os detalhes da ação na página
function displayStockDetails(stockDetails) {
    const detailsContainer = document.getElementById('stocks-list');

    // Limpa o conteúdo existente
    detailsContainer.innerHTML = '';

    // Verifica se stockDetails é um array e pega o primeiro elemento
    const stock = Array.isArray(stockDetails) ? stockDetails[0] : stockDetails;

    // Adiciona uma nova linha com os detalhes da ação
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${stock.codigo || 'N/A'}</td>
        <td>${stock.nome_empresa || 'N/A'}</td>
        <td>${stock.setor || 'N/A'}</td>
        <td>${stock.tipo || 'N/A'}</td>
        <td>${stock.cotacao || 'N/A'}</td>
        <td>${stock.div_yield || 'N/A'}</td>
        <td>${stock.pl || 'N/A'}</td>
        <td>${stock.patrim_liq || 'N/A'}</td>
        <td>${stock.valor_mercado || 'N/A'}</td>
        <td>${stock.data_ultima_cotacao || 'N/A'}</td>
        <td>${stock.receita_liquida_12m || 'N/A'}</td>
        <td>${stock.divida_liquida || 'N/A'}</td>
        <td>${stock.lucro_liquido_12m || 'N/A'}</td>
        <td>${stock.min_52_sem || 'N/A'}</td>
        <td>${stock.max_52_sem || 'N/A'}</td>
        <td>${stock.ebit_12m || 'N/A'}</td>
    `;
    
    detailsContainer.appendChild(row);
}

