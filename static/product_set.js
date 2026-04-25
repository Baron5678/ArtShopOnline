 document.addEventListener('DOMContentLoaded', function () {
    fetch('/products/json/')  // Make sure this URL matches your Django setup
    .then(response => response.json())
    .then(data => {
        const productsDiv = document.getElementById('products');
        data.forEach(product => {
            const productDetailUrl = `/products/${product.id}`; // Adjust URL based on your URL patterns
            const productDiv = document.createElement('div');
            const image = document.createElement('img');

            const ref_product = document.createElement('a')

            ref_product.href = productDetailUrl
            ref_product.appendChild(productDiv)

            image.src = product.image_url; // Set the source of the image
            image.alt = product.name; // Set the alt text as the product name
            image.style.width = '200px'; // Example of setting image size, adjust as needed
            image.style.height = 'auto';

            const title = document.createElement('h2');
            title.textContent = product.name;

            const description = document.createElement('p');
            description.textContent = product.description;

            const price = document.createElement('p');
            price.textContent = `Price: $${product.price}`;

            productDiv.className = 'product'
            productDiv.appendChild(image);
            productDiv.appendChild(title);
            productDiv.appendChild(description);
            productDiv.appendChild(price);

            productsDiv.appendChild(ref_product);
        });
    });
})