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
                    <td><a href="../detalhes/detalhes.html?codigo=${stock.codigo}">${stock.codigo}</a></td>
                    <td>${stock.nome_empresa}</td>
                    <td>${stock.setor}</td>
                    <td>${stock.tipo}</td>
                    <td>${stock.cotacao}</td>
                    <td>${stock.div_yield}</td>
                    <td>${stock.pl}</td>
                    <td>${stock.patrim_liq}</td>
                    <td>${stock.valor_de_mercado}</td>
                    <td>${stock.data_ultima_cotacao}</td>
                    <td>${stock.receita_liquida_12m}</td>
                    <td>${stock.divida_liquida}</td>
                    <td>${stock.valor_de_mercado}</td>
                    <td>${stock.lucro_liquido_12m}</td>
                    <td>${stock.patrim_liq}</td>
                    <td>${stock.min_52_sem}</td>
                    <td>${stock.max_52_sem}</td>
                    <td>${stock.ebit_12m}</td>
                    <td>${stock.data_ultima_cotacao}</td>
                   
                `;
                stocksList.appendChild(row);
            });
        })
        .catch(error => {
            stocksList.innerHTML = `<tr><td colspan="10">${error.message}</td></tr>`;
        });
});