// like-system.js
document.addEventListener('DOMContentLoaded', function() {

    initializeLikeSystem();
    
    // Initialize like buttons
    const likeButtons = document.querySelectorAll('.favorite-btn');
    
    likeButtons.forEach(button => {
        const productId = getProductIdFromUrl();
        
        // Show the button
        button.classList.remove('d-none');
        
        // Check if product is already liked
        if (isProductLiked(productId)) {
            button.innerHTML = '<i class="fa-solid fa-heart"></i>';
            button.classList.add('liked');
        } else {
            button.innerHTML = '<i class="fa-regular fa-heart"></i>';
            button.classList.remove('liked');
        }
        
        // Add click event
        button.addEventListener('click', toggleLike);
    });
});

function getProductIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function toggleLike(event) {
    event.preventDefault();
    
    const button = event.currentTarget;
    const productId = getProductIdFromUrl();
    
    if (isProductLiked(productId)) {
        // Unlike
        unlikeProduct(productId);
        button.innerHTML = '<i class="fa-regular fa-heart"></i>';
        button.classList.remove('liked');
    } else {
        // Like
        likeProduct(productId);
        button.innerHTML = '<i class="fa-solid fa-heart"></i>';
        button.classList.add('liked');
    }
}

function likeProduct(productId) {
    const likedProducts = getLikedProducts();
    likedProducts.push(productId);
    localStorage.setItem('likedProducts', JSON.stringify(likedProducts));
}

function unlikeProduct(productId) {
    let likedProducts = getLikedProducts();
    likedProducts = likedProducts.filter(id => id !== productId);
    localStorage.setItem('likedProducts', JSON.stringify(likedProducts));
}

function isProductLiked(productId) {
    const likedProducts = getLikedProducts();
    return likedProducts.includes(productId);
}

function getLikedProducts() {
    const likedProducts = localStorage.getItem('likedProducts');
    return likedProducts ? JSON.parse(likedProducts) : [];
}

function initializeLikeSystem() {
    // Initialize like buttons
    const likeButtons = document.querySelectorAll('.favorite-btn');
    
    likeButtons.forEach(button => {
        const productId = getProductIdFromUrl();
        
        // Show the button
        button.classList.remove('d-none');
        
        // Check if product is already liked
        if (isProductLiked(productId)) {
            button.innerHTML = '<i class="fa-solid fa-heart"></i>';
            button.classList.add('liked');
        } else {
            button.innerHTML = '<i class="fa-regular fa-heart"></i>';
            button.classList.remove('liked');
        }
        
        // Remove existing event listeners (important!)
        button.removeEventListener('click', toggleLike);
        
        // Add click event
        button.addEventListener('click', toggleLike);
    });
}