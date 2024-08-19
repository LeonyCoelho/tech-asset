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
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.textContent = sector.name;
                    li.setAttribute('data-id', sector.id); // Adicionar data-id ao elemento li

                    li.onclick = function() {
                        showSubsectors(sector.id);
                    };

                    // Cria o botão de exclusão
                    const deleteButton = document.createElement('a');
                    deleteButton.className = 'btn btn-outline-danger btn-sm';
                    deleteButton.innerHTML = '<i class="nf nf-md-delete"></i>';
                    deleteButton.href = '#';
                    deleteButton.onclick = function(event) {
                        event.preventDefault();
                        deleteSector(sector.id);
                    };

                    // Adiciona o botão de exclusão ao item da lista
                    li.appendChild(deleteButton);
                    sectorList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao carregar os setores:', error));
    }

    function deleteSector(sectorId) {
        console.log("Deletar setor com ID:", sectorId);

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


        fetch(`/preferences/sector/delete/${sectorId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({
                csrfmiddlewaretoken: csrfToken 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Setor deletado com sucesso:", sectorId);
                // Remover o setor do DOM
                document.querySelector(`#sector-list li[data-id='${sectorId}']`).remove();
                // Limpar a lista de subsetores ao deletar o setor
                document.getElementById('subsector-list').innerHTML = '';
            } else {
                console.log("Erro ao deletar o setor:", sectorId);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar a solicitação de exclusão:", error);
        });
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
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.textContent = subsector.name;
                    li.setAttribute('data-id', subsector.id); // Adicionar data-id ao elemento li

                    // Cria o botão de exclusão
                    const deleteButton = document.createElement('a');
                    deleteButton.className = 'btn btn-outline-danger btn-sm';
                    deleteButton.innerHTML = '<i class="nf nf-md-delete"></i>';
                    deleteButton.href = '#';
                    deleteButton.onclick = function(event) {
                        event.preventDefault();
                        deleteSubsector(subsector.id);
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

    function deleteSubsector(subsectorId) {
        console.log("Deletar subsector com ID:", subsectorId);

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


        fetch(`/preferences/subsector/delete/${subsectorId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({
                csrfmiddlewaretoken: csrfToken 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Subsector deletado com sucesso:", subsectorId);
                // Remover o subsetor do DOM
                document.querySelector(`#subsector-list li[data-id='${subsectorId}']`).remove();
            } else {
                console.log("Erro ao deletar o subsector:", subsectorId);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar a solicitação de exclusão:", error);
        });
    }

    // Evento para criar novo setor
    document.getElementById('new-sector-form').addEventListener('submit', function(event) {

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        event.preventDefault();
        const formData = new FormData(this);
        fetch(urls.newSector, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken 
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadSectors();
                this.reset(); // Limpar o formulário
            } else {
                console.log("Erro ao criar novo setor", data.errors);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar o formulário de novo setor:", error);
        });
    });

    // Evento para criar novo subsetor
    document.getElementById('new-subsector-form').addEventListener('submit', function(event) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


        event.preventDefault();
        const formData = new FormData(this);
        fetch(urls.newSubsector, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken 
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const sectorId = this.querySelector('select[name="parent"]').value;
                showSubsectors(sectorId);
                this.reset(); // Limpar o formulário
            } else {
                console.log("Erro ao criar novo subsetor", data.errors);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar o formulário de novo subsetor:", error);
        });
    });
});