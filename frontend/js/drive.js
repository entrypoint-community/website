document.addEventListener('DOMContentLoaded', function() {
    const fileStructure = {
        'Projects': {
            'Nginx Deployment': {
                'Kubernetes.txt': null,
                'Helm.txt': null
            },
            'Flask Application': {
                'main.py': null
            },
            'instructions.txt': null
        },
        'CV Examples': {
            'cv_template_1.txt': null
        },
        'contributers.txt': null
    };

    let path = [];

    function createFileTree(container, files) {
        container.innerHTML = ''; // Clear previous contents
        Object.keys(files).forEach(key => {
            const card = document.createElement('div');
            card.className = 'card square-card';
            card.style.backgroundColor = files[key] === null ? '#17a2b8' : '#ffc107'; // Blue for files, Yellow for folders
            
            const cardBody = document.createElement('div');
            cardBody.className = 'card-body';

            const icon = document.createElement('i');
            icon.className = files[key] === null ? 'far fa-file' : 'far fa-folder';
            const text = document.createElement('span');
            text.textContent = ' ' + key;

            if (files[key] !== null) { // If it's a folder
                cardBody.style.cursor = 'pointer';
                cardBody.addEventListener('click', () => {
                    path.push(key);
                    createFileTree(container, files[key]);
                    document.getElementById('backButton').style.display = 'inline-block';
                });
            }

            cardBody.appendChild(icon);
            cardBody.appendChild(text);
            card.appendChild(cardBody);
            container.appendChild(card);
        });
    }

    const backButton = document.getElementById('backButton');
    backButton.addEventListener('click', () => {
        path.pop();
        let currentData = fileStructure;
        path.forEach(p => { currentData = currentData[p]; });
        createFileTree(document.getElementById('driveContents'), currentData);
        if (path.length === 0) {
            backButton.style.display = 'none';
        }
    });

    const fileTree = document.getElementById('driveContents');
    createFileTree(fileTree, fileStructure);
});
