document.addEventListener('DOMContentLoaded', function() {
    const subsectorIdElement = document.getElementById('subsectorId');
    
    // Verificar se o elemento existe e capturar o valor de "data-value"
    if (subsectorIdElement) {
        const subsectorId = subsectorIdElement.getAttribute('data-value');
        
        // Log para verificar se o subsectorId está correto
        console.log('Sector ID capturado:', subsectorId);
        
        if (subsectorId) {
            console.log('Sector ID', subsectorId, 'encontrado.');
            populateKits(subsectorId); // Passa o subsectorId
            populateAssetTable(subsectorId); // Passa o subsectorId
        } else {
            console.error('Sector ID não encontrado no atributo data-value.');
        }
    } else {
        console.error('Elemento #subsectorId não encontrado no DOM.');
    }
});

function populateKits(subsectorId) {
    if (!subsectorId) {
        console.error('Sector ID indefinido para kits');
        return;
    }
    fetch(`/get_all_sector_kit/${subsectorId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar kits');
            }
            return response.json();
        })
        .then(data => {
            const listKit = document.getElementById('accordionKit');
            if (!listKit) {
                console.error('Elemento accordionKit não encontrado');
                return;
            }
            listKit.innerHTML = '';  // Limpar o conteúdo existente

            data.kit.forEach(kit => {
                const div = document.createElement('div');
                div.innerHTML = `
                    <div class="col-4">
                        <div class="card mb-3">
                            <div class="card-header">
                                <div class="row">
                                    <div class="col">
                                        ${kit.id} - ${kit.name}
                                    </div>
                                    <div class="col-auto">
                                        <span class="badge text-bg-secondary">${kit.assets.length}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <ul class="list-group">
                                    <li class="list-group-item">
                                        <a href="/kit/view/${kit.id}" class="btn btn-sm btn-secondary"><i class="nf nf-fa-eye"></i></a>
                                        <a class="btn btn-sm btn-secondary" data-bs-toggle="modal" data-bs-target="#transferKitModal${kit.id}"><i class="nf nf-fa-arrow_right_arrow_left"></i></a>
                                        <a class="btn btn-sm btn-secondary" data-bs-toggle="modal" data-bs-target="#editKitModal${kit.id}"><i class="nf nf-md-playlist_edit"></i></a>
                                        <button class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#deleteKitModal${kit.id}"><i class="nf nf-md-delete"></i></button>
                                    </li>
                                    ${kit.assets.length > 0 ? kit.assets.map(asset => `
                                        <li class="list-group-item" onclick="location.href='/asset/view/${asset.id}'" style="cursor: pointer;">
                                            ${asset.id} - ${asset.name} - ${asset.internal_code1}
                                        </li>
                                    `).join('') : '<div class="mt-2">Nenhum equipamento atribuído</div>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                `;
                listKit.appendChild(div);
            });
        })
        .catch(error => console.error('Erro ao carregar os kits:', error));
}

let currentPage = 1;
const rowsPerPage = 6; // Quantos ativos exibir por página

function populateAssetTable(id, page = 1) {
    fetch(`/get_assets_by_subsector/${id}/?page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar ativos');
            }
            return response.json();
        })
        .then(data => {
            const assets = data.assets;
            const tableBody = document.getElementById('assetTableBody');
            if (!tableBody) {
                console.error('Elemento assetTableBody não encontrado');
                return;
            }
            tableBody.innerHTML = ''; // Limpar o conteúdo existente da tabela

            if (assets.length > 0) {
                assets.forEach(asset => {
                    const row = document.createElement('tr');

                    row.innerHTML = `
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.id}</td>
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.internal_code1}</td>
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.name}</td>
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.sector || ''}</td>
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.subsector || ''}</td>
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.category || ''}</td>
                        <td onclick="window.location.href='/asset/view/${asset.id}'">${asset.subcategory || ''}</td>
                        <td>
                            <a href="/asset/view/${asset.id}" class="btn btn-sm btn-secondary"><i class="nf nf-fa-eye"></i></a>
                            <a href="/asset/edit/${asset.id}" class="btn btn-sm btn-secondary"><i class="nf nf-md-playlist_edit"></i></a>
                            ${asset.kit ? `<a class="btn btn-sm btn-secondary" href="/kit/view/${asset.kit.id}"><i class="nf nf-md-sitemap"></i></a>` : `
                            <a class="btn btn-sm btn-secondary" data-bs-toggle="modal" data-bs-target="#transferModalAsset${asset.id}"><i class="nf nf-fa-arrow_right_arrow_left"></i></a>`}
                            <button class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModalAsset${asset.id}"><i class="nf nf-md-delete"></i></button>
                        </td>
                    `;

                    tableBody.appendChild(row);
                });
            } else {
                tableBody.innerHTML = `<tr><td colspan="8" class="text-center">Nenhum equipamento no setor</td></tr>`;
            }

            // Renderizar paginação
            renderPagination(data.totalPages, page, id);
        })
        .catch(error => console.error('Erro ao carregar os ativos:', error));
}

function renderPagination(totalPages, currentPage, subsectorId) {
    const paginationContainer = document.getElementById('paginationContainer');
    
    if (!paginationContainer) {
        console.error('Elemento paginationContainer não encontrado');
        return;
    }

    paginationContainer.innerHTML = ''; // Limpar o conteúdo existente da paginação

    if (totalPages > 1) {
        // Botão de página anterior
        if (currentPage > 1) {
            const prevButton = document.createElement('button');
            prevButton.innerText = 'Anterior';
            prevButton.classList.add('btn', 'btn-sm', 'btn-secondary');
            prevButton.onclick = () => populateAssetTable(subsectorId, currentPage - 1);
            paginationContainer.appendChild(prevButton);
        }

        // Páginas numeradas
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.innerText = i;
            pageButton.classList.add('btn', 'btn-sm', 'btn-secondary');
            if (i === currentPage) {
                pageButton.classList.add('active'); // Adicionar classe se for a página atual
            }
            pageButton.onclick = () => populateAssetTable(subsectorId, i);
            paginationContainer.appendChild(pageButton);
        }

        // Botão de próxima página
        if (currentPage < totalPages) {
            const nextButton = document.createElement('button');
            nextButton.innerText = 'Próxima';
            nextButton.classList.add('btn', 'btn-sm', 'btn-secondary');
            nextButton.onclick = () => populateAssetTable(subsectorId, currentPage + 1);
            paginationContainer.appendChild(nextButton);
        }
    } else {
    }
}




document.addEventListener('DOMContentLoaded', function() {
    const subsectorId = document.getElementById('subsectorId').dataset.value;
    populateKits(subsectorId);
    // populateAssetTable(subsectorId, 1);
    
});

function updateSubSectorSummary(subsectorId) {
    fetch(`/api/subsector_summary/${subsectorId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar dados do setor');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Erro:', data.error);
                return;
            }

            // Atualizar os elementos HTML com os dados obtidos
            document.getElementById('subsectorName').innerText = data.subsector_name;
            document.getElementById('totalAssets').innerText = data.total_assets;
            document.getElementById('totalKits').innerText = data.total_kits;
        })
        .catch(error => console.error('Erro ao atualizar resumo do setor:', error));
}

// Mover o código dentro do DOMContentLoaded
document.addEventListener("DOMContentLoaded", function() {
    const subsectorSummaryDiv = document.querySelector(".subsector-summary");
    const subsectorId = subsectorSummaryDiv.getAttribute("data-subsector-id");

    updateSubSectorSummary(subsectorId);
});




function deleteKit(kitId) {
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
            const subsectorIdElement = document.getElementById('subsectorId');
            const subsectorId = subsectorIdElement ? subsectorIdElement.getAttribute('data-value') : null;

            // Atualize a tabela de assets
            if (subsectorId) {
                populateKits(subsectorId);
                populateAssetTable(subsectorId);
                updateSubSectorSummary(subsectorId);
            } else {
                console.error('Sector ID não encontrado ao atualizar os assets.');
            }

            // Fechar o modal do kit após a exclusão
            const modal = bootstrap.Modal.getInstance(document.getElementById(`deleteModal${kitId}`));
            if (modal) {
                modal.hide();
            }
        } else {
            console.error('Erro ao deletar o kit');
        }
    })
    .catch(error => {
        console.error('Error:', error);
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
            // populateAssetTable(); // Atualiza a tabela de ativos

            // Obtenha o subsectorId da página
            const subsectorIdElement = document.getElementById('subsectorId');
            const subsectorId = subsectorIdElement ? subsectorIdElement.getAttribute('data-value') : null;

            // Atualize a tabela de kits
            if (subsectorId) {
                populateKits(subsectorId);
                updateSubSectorSummary(subsectorId);
            } else {
                console.error('Sector ID não encontrado ao atualizar os kits.');
            }
            


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
    event.preventDefault();
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
            // Obtenha o subsectorId da página
            const subsectorIdElement = document.getElementById('subsectorId');
            const subsectorId = subsectorIdElement ? subsectorIdElement.getAttribute('data-value') : null;

            // Atualize a tabela de kits
            if (subsectorId) {
                populateKits(subsectorId);
                updateSubSectorSummary(subsectorId);
            } else {
                console.error('Sector ID não encontrado ao atualizar os kits.');
            }
            // populateAssetTable();
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
            // Obtenha o subsectorId da página
            const subsectorIdElement = document.getElementById('subsectorId');
            const subsectorId = subsectorIdElement ? subsectorIdElement.getAttribute('data-value') : null;
 
            // Atualize a tabela de kits
            if (subsectorId) {
                populateKits(subsectorId);
            } else {
                console.error('Sector ID não encontrado ao atualizar os kits.');
            }
            // populateAssetTable();
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

function transferAsset(event, assetId) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const form = document.getElementById(`transferAssetForm${assetId}`);
    const formData = new FormData(form);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Extrair o subsectorId do campo de seleção do formulário
    const subsectorId = formData.get('sector'); // 'sector' é o nome do campo no formulário

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

            // Obtenha o subsectorId da página
            const subsectorIdElement = document.getElementById('subsectorId');
            const subsectorId = subsectorIdElement ? subsectorIdElement.getAttribute('data-value') : null;

            // Atualize a tabela de kits
            if (subsectorId) {
                populateAssetTable(subsectorId);
                updateSubSectorSummary(subsectorId);
            } else {
                console.error('Sector ID não encontrado ao atualizar os kits.');
            }
            


            // Fechar o modal se estiver aberto
            const modal = bootstrap.Modal.getInstance(document.getElementById(`transferModalAsset${assetId}`));
            modal.hide();

        } else {
            console.error('Error transferring asset');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false; // Impede o envio do formulário
}



function view_transferAsset(event, assetId) {
    console.log("view_transferAsset chamado para assetId:", assetId);
    transferAsset(event, assetId, function() {
        console.log("Transferência concluída, recarregando a página...");
    });
}

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
            // Obtenha o subsectorId da página
            const subsectorIdElement = document.getElementById('subsectorId');
            const subsectorId = subsectorIdElement ? subsectorIdElement.getAttribute('data-value') : null;

            // Atualize a tabela de assets
            if (subsectorId) {
                populateAssetTable(subsectorId);
                updateSubSectorSummary(subsectorId);
            } else {
                console.error('Sector ID não encontrado ao atualizar os assets.');
            }
            


            // Fechar o modal se estiver aberto
            const modal = bootstrap.Modal.getInstance(document.getElementById(`deleteModalAsset${assetId}`));
            modal.hide();
        }
    });
}