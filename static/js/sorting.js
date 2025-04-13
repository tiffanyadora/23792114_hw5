// sorting.js
document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('product-sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', sortProducts);
    }
});

function sortProducts() {
    const sortSelect = document.getElementById('product-sort');
    const sortValue = sortSelect.value;
    
    if (!sortValue) return;
    
    const productsContainer = document.querySelector('.product-flex');
    if (!productsContainer) return;
    
    // Get all product cards
    const productCards = Array.from(productsContainer.querySelectorAll('.product-card'));
    
    // Sort based on selected option
    productCards.sort((a, b) => {
        if (sortValue === 'price-asc') {
            return getPriceFromCard(a) - getPriceFromCard(b);
        } else if (sortValue === 'price-desc') {
            return getPriceFromCard(b) - getPriceFromCard(a);
        } else if (sortValue === 'rating-asc') {
            return getRatingFromCard(a) - getRatingFromCard(b);
        } else if (sortValue === 'rating-desc') {
            return getRatingFromCard(b) - getRatingFromCard(a);
        }
    });
    
    // Reappend in sorted order
    productCards.forEach(card => {
        productsContainer.appendChild(card);
    });
}

function getPriceFromCard(card) {
    const priceText = card.querySelector('.product-price').textContent;
    return parseFloat(priceText.replace('$', ''));
}

function getRatingFromCard(card) {
    const ratingText = card.querySelector('.product-rating span').textContent;
    return parseFloat(ratingText);
}