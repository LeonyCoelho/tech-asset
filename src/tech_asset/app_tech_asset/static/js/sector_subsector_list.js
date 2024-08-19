document.addEventListener('DOMContentLoaded', function() {
    loadSectors();

    function loadSectors() {
        fetch('/get_sectors/')
            .then(response => response.json())
            .then(data => {
                const sectorList = document.getElementById('sector-list');
                sectorList.innerHTML = ''; // Limpar lista de setores

                data.sectors.forEach(sector => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center li-hover sector-item';
                    li.textContent = sector.name;
                    li.setAttribute('data-id', sector.id); // Adicionar data-id ao elemento li

                    li.onclick = function() {
                        showSubsectors(sector.id);
                    };

                    // Cria o botão de exclusão
                    const deleteButton = document.createElement('a');
                    deleteButton.className = 'btn btn-secondary btn-sm';
                    deleteButton.innerHTML = '<i class="nf nf-fa-eye"></i>';
                    deleteButton.href = '#';
                    deleteButton.onclick = function(event) {
                        event.preventDefault();
                        location.href = `/sector/view/${sector.id}/`;
                    };

                    // Adiciona o botão de exclusão ao item da lista
                    li.appendChild(deleteButton);
                    sectorList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao carregar os setores:', error));
    }

    function showSubsectors(sectorId) {
        console.log("showSubsectors chamado para o setor:", sectorId);

        fetch(`/get_subsectors/${sectorId}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data); // Log the data for debugging
                const subsectorList = document.getElementById('subsector-list');
                subsectorList.innerHTML = ''; // Limpar lista de subsetores

                if (data.subsectors) {
                    data.subsectors.forEach(subsector => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item li-hover d-flex justify-content-between align-items-center sector-item';
                        li.textContent = subsector.name;
                        li.setAttribute('data-id', subsector.id); // Adicionar data-id ao elemento li

                        li.onclick = function() {
                            location.href = `/subsector/view/${subsector.id}/`; // Redirecionar para a URL correta
                        };

                        
                        // Cria o botão de exclusão
                        const deleteButton = document.createElement('a');
                        deleteButton.className = 'btn btn-secondary btn-sm';
                        deleteButton.innerHTML = '<i class="nf nf-fa-eye"></i>';
                        deleteButton.href = '#';
                        deleteButton.onclick = function(event) {
                            event.preventDefault();
                            location.href = `/subsector/view/${subsector.id}/`;
                        };

                        // Adiciona o botão de exclusão ao item da lista
                        li.appendChild(deleteButton);
                        subsectorList.appendChild(li);
                    });
                } else {
                    console.log("Nenhum subsetor encontrado para o setor:", sectorId);
                }
            })
            .catch(error => console.error('Erro ao carregar os subsetores:', error));
    }
});

document.getElementById('sector_search').addEventListener('input', function() {
    let filter = this.value.toLowerCase();
    let items = document.querySelectorAll('.sector-item');

    console.log('Itens encontrados:', items); // Adicione este log para depuração

    items.forEach(function(item) {
        let text = item.textContent.toLowerCase();
        if (text.includes(filter)) {
            item.style.display = 'block'; // Use 'block' para garantir que o item seja exibido
        } else {
            item.style.display = 'none';
        }
    });
});
