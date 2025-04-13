document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const adminToolsBtn = document.getElementById('admin-tools');
    const modal = document.getElementById('product-submission-modal');
    const closeBtn = modal.querySelector('.close-modal');
    const cancelBtn = modal.querySelector('.cancel-btn');
    const form = document.getElementById('product-submission-form');
    
    // Show modal when admin tools button is clicked
    adminToolsBtn.addEventListener('click', function(e) {
      e.preventDefault();
      modal.style.display = 'block';
    });
    
    // Close modal when X button is clicked
    closeBtn.addEventListener('click', function() {
      modal.style.display = 'none';
    });
    
    // Close modal when Cancel button is clicked
    cancelBtn.addEventListener('click', function() {
      modal.style.display = 'none';
    });
    
    // Close modal when clicking outside the modal content
    window.addEventListener('click', function(e) {
      if (e.target === modal) {
        modal.style.display = 'none';
      }
    });
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const name = form.querySelector('[name="name"]').value;
        const category = form.querySelector('[name="category"]').value;
        const price = form.querySelector('[name="price"]').value;
        const rating = form.querySelector('[name="rating"]').value;
        const description = form.querySelector('[name="description"]').value;
        const features = form.querySelector('[name="features"]').value;
        const imageName = form.querySelector('[name="imageName"]').value;
        
        // Create new product ID
        const nextId = getNextProductId().toString();
        
        // Send data to server
        fetch('/api/add-product/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: nextId,
            name: name,
            description: description,
            features: features,
            rating: rating,
            price: price,
            category: category,
            imageName: imageName
        })
        })
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            // Create new product object for client-side
            const newProduct = {
            ID: nextId,
            Name: name,
            Description: description,
            Feature: features,
            Average_Rating: rating,
            Price: price,
            Category: category,
            imageName: imageName
            };
            
            // Add the new product to our client-side data
            addNewProduct(newProduct);
            
            // Update the UI with the new product
            updateProductsDisplay();
            
            // Reset form and close modal
            form.reset();
            modal.style.display = 'none';
            
            // Show success notification
            showNotification('Product added successfully!');
        } else {
            showNotification('Error: ' + (data.error || 'Unknown error'));
        }
        })
        .catch(error => {
        console.error('Error:', error);
        showNotification('Error saving product. See console for details.');
        });
    });
    
    // Function to display a notification
    function showNotification(message) {
      const notification = document.createElement('div');
      notification.className = 'notification';
      notification.textContent = message;
      
      document.body.appendChild(notification);
      
      // Style the notification
      notification.style.position = 'fixed';
      notification.style.bottom = '20px';
      notification.style.right = '20px';
      notification.style.backgroundColor = '#4CAF50';
      notification.style.color = 'white';
      notification.style.padding = '15px';
      notification.style.borderRadius = '5px';
      notification.style.zIndex = '1000';
      
      // Remove notification after 3 seconds
      setTimeout(() => {
        notification.remove();
      }, 3000);
    }
    
    // Function to update the products display on the page
    function updateProductsDisplay() {
      const productContainer = document.querySelector('.product-flex');
      
      // If we're on the home page and the product container exists
      if (productContainer) {
        // Format the new product for display
        const formattedProduct = formatProductForDisplay(productsData[productsData.length - 1]);
        
        // Create new product card
        const productCard = document.createElement('a');
        productCard.href = `/products/?id=${formattedProduct.product_id}`;
        productCard.className = 'product-card';
        productCard.setAttribute('data-product-id', formattedProduct.product_id);
        
        // Add click event to handle dynamic navigation
        productCard.addEventListener('click', function(e) {
          e.preventDefault();
          navigateToProduct(formattedProduct.product_id);
        });
        
        // Create product card HTML
        productCard.innerHTML = `
          <div class="product-image">
            <img src="/static/images/${formattedProduct.get_image_name()}" alt="${formattedProduct.name}">
          </div>
          <div class="product-info p-3">
            <h3 class="mb-1">${formattedProduct.name}</h3>
            <p class="product-price">$${formattedProduct.price}</p>
            <div class="product-rating d-flex align-center mb-1">
              ${generateStarRating(formattedProduct.rating)}
              <span class="ml-1">${formattedProduct.rating}</span>
            </div>
          </div>
        `;
        
        // Add the new product card to the container
        productContainer.appendChild(productCard);
      }
    }
    
    // Helper function to generate star rating HTML
    function generateStarRating(rating) {
      const fullStars = Math.floor(rating);
      const hasHalfStar = rating % 1 >= 0.5;
      let starsHtml = '';
      
      // Add full stars
      for (let i = 0; i < fullStars; i++) {
        starsHtml += '<i class="fa-solid fa-star"></i>';
      }
      
      // Add half star if needed
      if (hasHalfStar) {
        starsHtml += '<i class="fa-solid fa-star-half-alt"></i>';
      }
      
      return starsHtml;
    }
  });