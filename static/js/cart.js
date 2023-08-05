function addToCart(element, book_id) {
    const cart = document.getElementById("cart_top")
    const cart_count = document.getElementById("cart_top_count")
    const cart_count_items = document.getElementById("cart_top_count_items")
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
        result => cart_count_items.innerHTML = result.result,
        cart.classList.remove("btn-outline-secondary"),
        cart.classList.add("btn-outline-danger"),
        cart_count.classList.remove("d-none"),
    )
    .catch(
        error => console.log(error)
    );
}

function removeFromCart(element, book_id) {
    const cart = document.getElementById("cart_top")
    const cart_count = document.getElementById("cart_top_count")
    const cart_count_items = document.getElementById("cart_top_count_items")
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
        result => cart_count_items.innerHTML = result.result,
        element.parentElement.parentElement.remove(),
        cart.classList.remove("btn-outline-secondary"),
        cart.classList.add("btn-outline-danger"),
        cart_count.classList.remove("d-none"), // TODO: check if cart is empty
    )
    .catch(
        error => console.log(error)
    );
}
