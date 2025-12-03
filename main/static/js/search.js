// Enhanced Search with Auto-suggestions
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.createElement('div');
    searchResults.className = 'search-suggestions';
    searchResults.style.display = 'none';

    if (searchInput) {
        searchInput.parentElement.appendChild(searchResults);

        let searchTimeout;

        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            const query = this.value.trim();

            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }

            searchTimeout = setTimeout(() => {
                fetchSearchSuggestions(query);
            }, 300);
        });

        // Close suggestions when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }

    async function fetchSearchSuggestions(query) {
        try {
            const response = await fetch(`/api/products/?search=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (data.results && data.results.length > 0) {
                displaySuggestions(data.results.slice(0, 5));
            } else {
                searchResults.innerHTML = '<div class="no-results">No products found</div>';
                searchResults.style.display = 'block';
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    function displaySuggestions(products) {
        let html = '<div class="suggestions-header">Suggestions</div>';

        products.forEach(product => {
            html += `
                <a href="/product/${product.id}/" class="suggestion-item">
                    <img src="${product.image || '/static/images/placeholder.png'}" alt="${product.name}">
                    <div class="suggestion-details">
                        <div class="suggestion-name">${product.name}</div>
                        <div class="suggestion-price">$${product.price}</div>
                    </div>
                </a>
            `;
        });

        html += `<a href="/products/?search=${encodeURIComponent(searchInput.value)}" class="view-all-results">View All Results →</a>`;

        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
    }
});
