document.getElementById('refreshButton').addEventListener('click', loadContainers);

function loadContainers() {
    const tableContainer = document.querySelector('.table-container');
    const loadingOverlay = document.getElementById('loading');
    
    // Afficher l'indicateur de chargement
    loadingOverlay.style.display = 'flex';
    tableContainer.classList.add('loading');

    fetch('/containers')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('containersTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = '';

            data.forEach(container => {
                const row = document.createElement('tr');

                const nameCell = document.createElement('td');
                nameCell.textContent = container.name;
                row.appendChild(nameCell);

                const idCell = document.createElement('td');
                idCell.textContent = container.id;
                row.appendChild(idCell);

                const imageCell = document.createElement('td');
                imageCell.textContent = container.image;
                row.appendChild(imageCell);

                const ipCell = document.createElement('td');
                ipCell.textContent = container.ip_address;
                row.appendChild(ipCell);

                const portCell = document.createElement('td');
                portCell.textContent = container.port;
                row.appendChild(portCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching containers:', error);
        })
        .finally(() => {
            // Simuler un délai supplémentaire avant de masquer l'indicateur de chargement
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
                tableContainer.classList.remove('loading');
            }, 500); // Délai de 500 ms avant de masquer l'animation
        });
}

// Chargement initial des conteneurs
loadContainers();
