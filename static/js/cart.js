function addToCart(element, book_id) {
    const url = element.dataset.url

    let data = new FormData()
    data.append("book_id", book_id)
    data.append("quantity", 1)

    fetch(url, {
        "method": "POST",
        "body": data,
        })
    .then(response => response.json())
    .then(
        result => updateCartElements(result, "update")
    )
    .catch(
        error => console.log(error)
    );
}

function removeFromCart(element, book_id) {
    const url = element.dataset.url

    let data = new FormData()
    data.append("book_id", book_id)
    data.append("quantity", 1)

    fetch(url, {
        "method": "POST",
        "body": data,
        })
    .then(response => response.json())
    .then(
        result => updateCartElements(result, "remove"),
        element.parentElement.parentElement.remove(),
    )
    .catch(
        error => console.log(error)
    );
}

function updateCartElements(result, action="remove") {
    const cart = document.getElementById("cart_top")
    const cart_count = document.getElementById("cart_top_count")
    const cart_count_items = document.getElementById("cart_top_count_items")

    cart_count_items.innerHTML = result.result;

    if (action == "remove") {
        cart.classList.remove("btn-outline-secondary"),
        cart.classList.add("btn-outline-danger"),
        cart_count.classList.remove("d-none")
        if (result.result == 0) {
            cart.classList.remove("btn-outline-danger"),
            cart.classList.add("btn-outline-secondary"),
            cart_count.classList.add("d-none")
        }
    } else if (action == "update") {
        cart.classList.remove("btn-outline-secondary"),
        cart.classList.add("btn-outline-danger"),
        cart_count.classList.remove("d-none")
    };
}
