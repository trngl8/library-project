function updateOrderElements(result) {
    const confirmButton = document.getElementById("confirm_button")
    const spinnerLoader = document.getElementById("spinner_loader")
    if (result.status == "success") {
        confirmButton.classList.remove("btn-primary"),
        confirmButton.classList.add("btn-success")
        confirmButton.innerHTML = "Confirmed"
        spinnerLoader.classList.add("d-none")
    }
}

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
        result => updateOrderElements(result)
    )
    .catch(
        error => console.log(error)
    );
}
