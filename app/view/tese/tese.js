const codigo = localStorage.getItem('codigo');
// Função para buscar parâmetros da URL
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}


// Função para carregar os detalhes da ação
function fetchStockDetailsForTese() {
    
    if (!codigo) {
        console.error('Nenhum código de ação fornecido.');
        document.body.innerHTML = '<h1>Erro: Código da ação não encontrado</h1>';
        return;
    }

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
            displayStockDetailsForTese(stockDetails);
        })
        .catch(error => {
            console.error(error.message);
            document.body.innerHTML = `<h1>Erro: ${error.message}</h1>`;
        });
}

// Função para exibir os detalhes da ação na tela de tese
function displayStockDetailsForTese(stockDetails) {
    document.querySelector('header h2').textContent += `: ${codigo}`;
}

// Função para lidar com o envio do formulário
document.getElementById("tese-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Evita o reload da página
    console.log(codigo);
    // Captura os valores inseridos pelo usuário
    const plUsuario = document.getElementById("plUsuario").value.trim();
    const pvpUsuario = document.getElementById("pvpUsuario").value.trim();

    if (!codigo) {
        alert("Código da ação não encontrado.");
        return;
    }

    document.getElementById("loading-container").style.display = "block";

    // Monta o objeto de payload dinamicamente
    const payload = {};
    if (plUsuario) payload.pl = parseFloat(plUsuario);
    if (pvpUsuario) payload.pvp = parseFloat(pvpUsuario);

    console.log(JSON.stringify(payload));

    try {
        // Enviar os dados para a API
        const response = await fetch(`http://127.0.0.1:5000/api/gerarTese?codigo=${codigo}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error("Erro ao gerar tese. Verifique os dados fornecidos.");
        }

        const data = await response.json();
        console.log(typeof data.tese)
        console.log(data.vi)
        // Exibe os dados retornados pela API
        const resultadoDiv = document.getElementById("descricaoTese");
        resultadoDiv.innerHTML = `Tese gerada:\n\n${mmd(data.tese)}`;

        const resultadoVi = document.getElementById("viTese");
        resultadoVi.value = data.vi;

        console.log(mmd(data.tese))
    } catch (error) {
        console.error("Erro:", error.message);
        alert("Erro ao gerar tese. Tente novamente.");
    } finally {
        // Ocultar o loading após a resposta da API
        document.getElementById("loading-container").style.display = "none";
    }
});

// Função para voltar à página de detalhes
function voltar() {
    window.location.href= `../detalhes/detalhes.html?codigo=${codigo}`
}
