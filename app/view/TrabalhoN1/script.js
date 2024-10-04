document.addEventListener("DOMContentLoaded", function() {
    const stocksList = document.getElementById('stocks-list');

    const apiUrl = 'http://127.0.0.1:5000/detalhes';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar os dados');
            }
            return response.json();
        })
        .then(stocks => {
            console.log(stocks);
            stocksList.innerHTML = '';

            // Itera sobre cada ação (stock) retornada pela API
            stocks.forEach(stock => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${stock.codigo}</td>
                    <td>${stock.nome_empresa}</td>
                    <td>${stock.setor}</td>
                    <td>${stock.tipo}</td>
                    <td>${stock.cotacao}</td>
                    <td>${stock.div_yield}</td>
                    <td>${stock.pl}</td>
                    <td>${stock.patrim_liq}</td>
                    <td>${stock.valor_de_mercado}</td>
                    <td>${stock.data_ultima_cotacao}</td>
                `;
                stocksList.appendChild(row);
            });
        })
        .catch(error => {
            stocksList.innerHTML = `<tr><td colspan="10">${error.message}</td></tr>`;
        });
});
