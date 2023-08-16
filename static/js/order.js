function refreshOrder(element, order_id) {
    const url = element.dataset.url

    let data = new FormData()
    data.append("order_id", order_id)

    fetch(url, {
        "method": "POST",
        "body": data,
        })
    .then(response => response.json())
    .then(
        result => element.innerHTML = result.status
    )
    .catch(
        error => console.log(error)
    );
}
