function addToCart(productId, buttonElement) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", `/products/${productId}/add-to-cart`, true);
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    console.log("Sending request to add product:", productId);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                window.location.reload()
                console.log("Added to cart");
            } else {
                console.error("Request failed:", xhr.responseText);
            }
        }
    };
    xhr.send();
}

function removeFromCart(productId, buttonElement) {
    fetch(`/products/${productId}/remove-from-cart`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Request failed");
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "success") {
            const item = buttonElement.closest("li");
            if (data.amount === 0) {
                item.remove();
            } else {
                const amountElement = item.querySelector(".amount");
                if (amountElement) {
                    amountElement.textContent = `Amount: ${data.amount}`;
                }

                const totalElement = item.querySelector(".total");
                if (totalElement) {
                    totalElement.textContent = `Total: ${data.amount * data.price} $`;
                }
            }
             const cartList = document.getElementById("cart-list");
             if (cartList && cartList.children.length === 0) {
                    cartList.innerHTML = "<p>No products</p>";
             }
        } else {
            alert(data.message);
        }
        window.location.reload();
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-for-event").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId
            console.log("Remove:", productId);
            removeFromCart(productId, this);
        });
    });

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId;
            console.log("Add:", productId);
            addToCart(productId, this);
        });
    });
});
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