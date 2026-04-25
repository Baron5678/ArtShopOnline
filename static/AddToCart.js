function addToCartFunction() {
    let productId = document.getElementById('addToCart').getAttribute('data-product-id');
    let xhr = new XMLHttpRequest();


    xhr.open("POST", `/products/${productId}/add-to-cart`, true);

    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // CSRF token

    // Handle the response
    xhr.onreadystatechange = function () {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // Change the border of the button to be bold
            let addToCartButton = document.getElementById('addToCart');
            addToCartButton.style.border = "2px solid"; // Example: 2px solid border

            // Redirect to the product page
            window.location.href = `/products/${productId}`;
        }
    }

    // Send the request without a JSON payload
    xhr.send();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}