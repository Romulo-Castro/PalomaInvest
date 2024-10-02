document.addEventListener("DOMContentLoaded", function() {
    const stocksList = document.getElementById('stocks-list');

    // Exemplo de API, você deve substituir pela sua API real
    const apiUrl = 'stocks.json'; // Use o JSON local para teste

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar os dados');
            }
            return response.json();
        })
        .then(data => {
            // Supondo que a resposta tenha um array de ações
            const stocks = data.stocks;

            // Limpa a lista antes de adicionar novos dados
            stocksList.innerHTML = '';

            stocks.forEach(stock => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${stock.name}</td>
                    <td>${stock.price.toFixed(2)}</td>
                    <td>${stock.setor}</td>
                `;
                stocksList.appendChild(row);
            });
        })
        .catch(error => {
            stocksList.innerHTML = `<tr><td colspan="2">${error.message}</td></tr>`;
        });
});
