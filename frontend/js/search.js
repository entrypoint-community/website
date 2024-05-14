document.addEventListener('DOMContentLoaded', function() {
    console.log("here")
    function searchPosts() {
        const searchInput = document.getElementById('searchInput');
        const term = searchInput.value.toLowerCase();
        const posts = document.querySelectorAll('#postsContainer .blog-post');

        posts.forEach(post => {
            const title = post.querySelector('h5') ? post.querySelector('h5').textContent.toLowerCase() : '';
            const summary = post.querySelector('p') ? post.querySelector('p').textContent.toLowerCase() : '';

            if (title.includes(term) || summary.includes(term)) {
                post.style.display = '';  // Show the post
            } else {
                post.style.display = 'none';  // Hide the post
            }
        });
    }

    const searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission
        searchPosts();
    });
});
