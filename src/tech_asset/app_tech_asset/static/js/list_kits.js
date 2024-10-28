function populateKits() {
    fetch('/get_all_kits/')
        .then(response => response.json())
        .then(data => {
            const listKit = document.getElementById('accordionKit');
            listKit.innerHTML = '';  // Limpar o conteúdo existente

            data.kit.forEach(kit => {
                const div = document.createElement('div');
                div.classList.add('accordion-item', 'accord-kit');
                div.innerHTML = `
                    <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${kit.id}" aria-expanded="false" aria-controls="collapse${kit.id}">
                            ${kit.id} - ${kit.name} - ${kit.sectors} | ${kit.subsectors}
                        </button>
                    </h2>
                    <div id="collapse${kit.id}" class="accordion-collapse collapse" data-bs-parent="#accordionKit">
                        <div class="accordion-body">
                            <ul class="list-group">
                                <li class="list-group-item">
                                    <a href="/kit/view/${kit.id}" class="btn btn-sm btn-secondary"><i class="nf nf-fa-eye"></i></a>
                                    <a class="btn btn-sm btn-secondary" data-bs-toggle="modal" data-bs-target="#transferKitModal${kit.id}"><i class="nf nf-fa-arrow_right_arrow_left"></i></a>
                                    <a class="btn btn-sm btn-secondary" data-bs-toggle="modal" data-bs-target="#editKitModal${kit.id}"><i class="nf nf-md-playlist_edit"></i></a>
                                    <button class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#deleteKitModal${kit.id}"><i class="nf nf-md-delete"></i></button>
                                </li>
                                    ${kit.assets.map(asset => `
                                        <li class="list-group-item" onclick="location.href='/asset/view/${asset.id}'" style="cursor: pointer;">${asset.id} - ${asset.name} - ${asset.internal_code1}</li>
                                    `).join('')}
                            </ul>
                        </div>
                    </div>
                `;
                listKit.appendChild(div);
            });
        })
        .catch(error => console.error('Erro ao carregar os kits:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    populateKits();
});

function deleteKit(event, kitId) {
    event.preventDefault(); // Impede o envio padrão do formulário
    console.log('Kit', kitId, 'will be deleted');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(`/kit/delete/${kitId}/`, {
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
            populateKits();  // Agora a função deve estar acessível
            const modal = bootstrap.Modal.getInstance(document.getElementById(`transferModal${assetId}`));
            modal.hide();
        }
    });
}

function transferKit(event, kitId, callback) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Obtenha o formulário correto usando o ID
    const form = document.getElementById(`transferForm${kitId}`);
    const sectorValue = form.querySelector('select[name="sector"]').value;
    const subsectorValue = form.querySelector('select[name="subsector"]').value;

    console.log(`Selected sector: ${sectorValue}`);
    console.log(`Selected subsector: ${subsectorValue}`);

    if (!form) {
        console.error(`Formulário com ID transferForm${kitId} não encontrado.`);
        return false;
    } 

    const formData = new FormData(form);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Fazer a requisição para transferir o kit
    fetch(`/kit/transfer/${kitId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData // Envia os dados do formulário
    })
    .then(response => {
        if (response.ok) {
            console.log('Kit transferido com sucesso');
            populateAssetTable(); // Atualiza a tabela de ativos
            populateKits(); // Atualiza a tabela de kits
            
            // Fechar o modal se estiver aberto
            const modal = bootstrap.Modal.getInstance(document.getElementById(`transferModal${kitId}`));
            modal.hide();

            // Chame o callback, se houver
            if (typeof callback === 'function') {
                callback();
            }
        } else {
            console.error('Erro ao transferir kit');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });

    return false; // Impede o envio do formulário
}


function view_transferKit(event, kitId) {
    console.log("view_transferKit chamado para kitId:", kitId);
    transferKit(event, kitId, function() {
        console.log("Transferência concluída, recarregando a página...");
    });
    setTimeout(function() {
        location.reload();
    }, 500);
}


function view_deleteKit(event, kitId) {
    console.log('View_Kit Delete');
    console.log('Kit', kitId, 'will be deleted');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    fetch(`/kit/view/delete/${kitId}/`, {
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
            window.location.href = '/';  // Redireciona para /home se a resposta for bem-sucedida
        } else {
            console.error('Erro ao deletar o kit');
        }
    })
    .catch(error => {
        console.error('Ocorreu um erro:', error);
    });

    return false;
}



function editKit(event, kitId){
    event.preventDefault();
    const form = document.getElementById(`editForm${kitId}`);
    if (!form) {
        console.error(`Formulario com ID transferForm${kitId} nao encontrado`);
        return false;
    }

    const formData = new FormData(form);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(`/kit/edit/${kitId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            populateKits();
            populateAssetTable();
        } else {
            console.error('Erro ao editar Kit')
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
    return false;
}


function view_editKit(event, kitId) {
    event.preventDefault();
    const form = document.getElementById(`editForm${kitId}`);
    if (!form) {
        console.error(`Formulario com ID ${kitId} nao encontrado`);
        return false;
    }

    const formData = new FormData(form);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(`/kit/edit/${kitId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.reload(); // Recarregar a página se a resposta for bem-sucedida
        } else {
            console.error('Erro ao editar Kit');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
    return false;
}
