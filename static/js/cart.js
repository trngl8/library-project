function addToCart(el, book_id) {
  const cart = document.getElementById("cart_top")
  const cart_count = document.getElementById("cart_top_count")
  const cart_count_items = document.getElementById("cart_top_count_items")
  const order_button = document.getElementById("order_button")
  const url = order_button.dataset.order_url
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
