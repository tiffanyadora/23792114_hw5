// static/js/search.js
document.addEventListener('DOMContentLoaded', () => {
    // Get all search forms (desktop & mobile)
    const searchForms = document.querySelectorAll('form[action$="search/"]');

    if (searchForms.length === 0) {
        console.warn("No search form found! Check if it's hidden in mobile.");
        return;
    }

    // Function to check if localStorage is available (for certain mobile browsers)
    function isLocalStorageAvailable() {
        try {
            localStorage.setItem('test', 'test');
            localStorage.removeItem('test');
            return true;
        } catch (e) {
            console.warn("localStorage is not available! Using sessionStorage instead.");
            return false;
        }
    }

    const storage = isLocalStorageAvailable() ? localStorage : sessionStorage;

    // Function to save recent searches
    function saveRecentSearch(query) {
        if (!query.trim()) return;

        let recentSearches = JSON.parse(storage.getItem('recentSearches') || '[]');

        // Remove duplicates and keep only the last 3 searches
        recentSearches = recentSearches.filter(search => search !== query);
        recentSearches.unshift(query);
        recentSearches = recentSearches.slice(0, 3);

        storage.setItem('recentSearches', JSON.stringify(recentSearches));

        // Update the recent searches display
        displayRecentSearches();
    }

    // Function to display recent searches in the UI
    function displayRecentSearches() {
        const recentSearchesContainer = document.getElementById('recent-search-buttons');
        if (!recentSearchesContainer) return;

        const recentSearches = JSON.parse(storage.getItem('recentSearches') || '[]');        

        recentSearchesContainer.innerHTML = '';

        recentSearches.forEach(query => {
            const button = document.createElement('button');
            button.textContent = query;
            button.classList.add('recent-search-btn');

            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Get the searchInput from the active form
                const activeSearchInput = document.querySelector('form[action$="search/"]:not(.hidden) input[name="query"]');
                if (activeSearchInput) {
                    activeSearchInput.value = query;
                    activeSearchInput.closest('form').submit();
                }
            });

            recentSearchesContainer.appendChild(button);
        });        
    }

    // Event listener for each search form (desktop & mobile)
    searchForms.forEach(searchForm => {
        searchForm.addEventListener('submit', (e) => {
            const searchInput = searchForm.querySelector('input[name="query"]');
            const query = searchInput.value.trim();

            if (query) {
                saveRecentSearch(query);
            }
        });
    });

    // When the page loads, display recent searches
    window.onload = function () {
        displayRecentSearches();

        // Set input to the last saved search
        searchForms.forEach(searchForm => {
            const searchInput = searchForm.querySelector('input[name="query"]');
            const lastQuery = JSON.parse(storage.getItem('recentSearches') || '[]')[0];

            if (lastQuery && searchInput) {
                searchInput.value = lastQuery;
            }
        });
    };
});
