// Definindo a função populateTable no escopo global
function populateAssetTable() {
    fetch('/get_all_assets/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('asset-table-body');
            tableBody.innerHTML = '';  // Limpar o conteúdo existente

            data.asset.forEach(asset => {
                const row = document.createElement('tr');
                row.innerHTML = `
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.id}</td>
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.internal_code1 || ''}</td>
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.name || ''}</td>
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.sector || ''}</td>
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.subsector || ''}</td>
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.category || ''}</td>
                <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.subcategory || ''}</td>
                <td>
                    <a href="/asset/view/${asset.id}" class="btn btn-sm btn-secondary"><i class="nf nf-fa-eye"></i></a>
                    <a href="/asset/edit/${asset.id}" class="btn btn-sm btn-secondary"><i class="nf nf-md-playlist_edit"></i></a>
                    <button class="btn btn-secondary btn-sm" id="generateQR${asset.id}" data-bs-toggle="modal" data-bs-target="#qrModal${asset.id}"><i class="nf nf-md-qrcode"></i></button>
                    ${asset.kit ? 
                        `<a class="btn btn-sm btn-secondary" href="/kit/view/${asset.kit.id}"><i class="nf nf-md-sitemap"></i></a>` : 
                        `<a class="btn btn-sm btn-secondary" data-bs-toggle="modal" data-bs-target="#transferAssetModal${asset.id}"><i class="nf nf-fa-arrow_right_arrow_left"></i></a>`
                    }
                    <button class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal${asset.id}"><i class="nf nf-md-delete"></i></button>
                </td>
            `;
            
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Erro ao carregar os ativos:', error));
}

// Adicionando um listener para garantir que a tabela seja populada quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    populateAssetTable();
});

function deleteAsset(assetId) {
    console.log('Asset', assetId, 'will be deleted');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(`/asset/delete/${assetId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
        },
        body: JSON.stringify({
            csrfmiddlewaretoken: csrfToken 
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('Deleted');
            populateKits(); // Atualiza a tabela
            populateAssetTable();  // Agora a função deve estar acessível
        }
    });
}

function transferAsset(event, assetId) {
    event.preventDefault(); // Impede o envio padrão do formulário
    console.log(assetId)
    const form = document.getElementById(`transferAssetForm${assetId}`);


    const formData = new FormData(form);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Fazer a requisição para transferir o ativo
    fetch(`/asset/transfer/${assetId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData // Envia os dados do formulário
    })
    .then(response => {
        if (response.ok) {
            console.log('Asset transferred successfully');
            populateAssetTable(); // Atualiza a tabela
        } else {
            console.error('Error transferring asset');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false; // Impede o envio do formulário
}
