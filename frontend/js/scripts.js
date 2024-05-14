import { API_KEY, CLIENT_ID, DISCOVERY_DOCS, SCOPES, API_BASE_URL } from "./consts.js";

document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    if (path.includes('posts.html')) {
        fetchBlogPosts();
        adjustPostContainerWidth();
    } else if (path.includes('dashboard.html')) {
        renderDashboardCharts();
    } else if (path.includes('members.html')) {
        fetchCommunityMembers();
    } else if (path.includes('drive.html')) {
        initializeDriveAPI();
    }
});

function adjustPostContainerWidth() {
    const sidePanel = document.querySelector('.side-panel'); // Adjust the selector as needed
    const postsContainer = document.querySelector('#home');
    if (sidePanel) {
        postsContainer.style.marginLeft = `${sidePanel.offsetWidth + 20}px`; // 20px for some extra spacing
    }
}

function fetchBlogPosts() {
    fetch(`${API_BASE_URL}/posts`)
        .then(response => response.json())
        .then(posts => {
            const postsContainer = document.querySelector('#postsContainer');
            posts.forEach(post => {
                const cardHtml = `
                    <div class="blog-post bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                        <img src="${post.image}" alt="Thumbnail" class="w-full h-48 object-cover"> <!-- Dynamic image source -->
                        <div class="p-4">
                            <h5 class="text-xl font-bold mb-2">${post.title}</h5>
                            <p class="text-gray-700 text-base mb-4">${post.summary}</p>
                            <div class="text-gray-600 text-sm mb-4">
                                <span>By ${post.author}</span> | <span>${new Date(post.date).toLocaleDateString()}</span>
                            </div>
                            <a href="${post.url}" class="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors duration-300">Read More</a>
                        </div>
                    </div>
                `;
                postsContainer.innerHTML += cardHtml;
            });
        })
        .catch(error => console.error('Error fetching blog posts:', error));
}


function renderDashboardCharts() {
    const ctx = document.getElementById('communitySizeChart').getContext('2d');
    const communitySizeChart = new Chart(ctx, {
        type: 'line', // Change to 'bar', 'line', etc. based on your preference
        data: {
            labels: ['January', 'February', 'March', 'April'],
            datasets: [{
                label: 'Community Size Over Time',
                data: [50, 100, 150, 200],
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function fetchCommunityMembers() {
    fetch(`${API_BASE_URL}/members`)
        .then(response => response.json())
        .then(members => {
            const membersContainer = document.querySelector('#members .grid');
            members.forEach(member => {
                const memberHtml = `
                    <div class="member-card col-span-1 bg-white p-4 shadow-lg rounded-lg text-center hover:shadow-xl transition-shadow duration-300 ease-in-out">
                        <img src="${member.photo}" alt="${member.name}" class="w-24 h-24 rounded-full mx-auto border-4 border-gray-300">
                        <h5 class="text-lg font-bold mt-4 text-indigo-600">${member.name}</h5>
                        <p class="title-position text-gray-600 mt-2">${member.position} &mdash; <span class="text-teal-500">${member.seniority} years</span> of expertise at <span class="font-semibold">${member.company}</span></p>
                    </div>
                `;
                
                membersContainer.innerHTML += memberHtml;
            });
        })
        .catch(error => console.error('Error fetching community members:', error));
}

function initializeDriveAPI() {
    gapi.load('client:auth2', () => {
        gapi.client.init({
            apiKey: API_KEY,
            clientId: CLIENT_ID,
            discoveryDocs: DISCOVERY_DOCS,
            scope: SCOPES
        }).then(() => {
            gapi.auth2.getAuthInstance().signIn().then(() => {
                listDriveFiles();
            });
        });
    });
}

function listDriveFiles() {
    gapi.client.drive.files.list({
        'pageSize': 10,
        'fields': "nextPageToken, files(id, name, mimeType, parents)"
    }).then(response => {
        const files = response.result.files;
        const filesContainer = document.getElementById('driveContents');
        files.forEach(file => {
            const fileHtml = `<p>${file.name}</p>`;
            filesContainer.innerHTML += fileHtml;
        });
    });
}
