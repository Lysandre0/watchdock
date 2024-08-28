document.getElementById('refreshButton').addEventListener('click', loadContainers);

function loadContainers() {
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

                const domainCell = document.createElement('td');
                domainCell.textContent = container.domain_name;
                row.appendChild(domainCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching containers:', error));
}

// Chargement initial des conteneurs
loadContainers();
