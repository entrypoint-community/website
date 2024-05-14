document.addEventListener('DOMContentLoaded', function() {
    const announcements = [
        { title: "Announcement Title", date: "3 days ago", summary: "Here is the first announcement...", detail: "More details..." },
        { title: "Second Announcement", date: "1 week ago", summary: "Here is the second announcement...", detail: "Additional information here..." }
    ];

    const list = document.getElementById('announcementList');
    announcements.forEach(announcement => {
        const col = document.createElement('div');
        col.className = 'col-12'; // Ensure each card spans the full width of the row
        const card = document.createElement('div');
        card.className = 'card announcement-card';
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title announcement-title">${announcement.title}</h5>
                <h6 class="card-subtitle mb-2 text-muted announcement-date">${announcement.date}</h6>
                <p class="card-text announcement-body">${announcement.summary}</p>
                <a href="#" class="card-link">Read more...</a>
            </div>
        `;
        col.appendChild(card);
        list.appendChild(col);
    });
});