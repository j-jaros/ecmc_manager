async function get_servers() {
    // pobranie statusow serwerow mc
    try {
        var resp = await fetch("/getServerStatus/all")
        resp = await resp.json()
        console.log(resp)
    } catch (e) {
        console.error(`Podczas proby pobrania statusow serwerow, wystapil blad: ${e}`)
    }

    display_servers(resp)
}


function display_servers(server_list) {
    for (let server_name in server_list) {
        let ping = server_list[server_name]
        const tr = document.createElement("tr")
        tr.setAttribute('server_name', server_name)

        const checkbox_td = document.createElement("td")
        const checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox_td.appendChild(checkbox)

        const name_td = document.createElement("td")
        name_td.textContent = server_name

        const status_td = document.createElement("td")
        const status = document.createElement("div")
        status_td.appendChild(status)

        console.log(ping)
        if (ping == -1) {
            status.classList.value = "off"
        } else {
            status.classList.value = "on"
        }

        tr.appendChild(checkbox_td)
        tr.appendChild(name_td)
        tr.appendChild(status_td)

        document.querySelector("#servers_table tbody").appendChild(tr)
    }
}

var allow_command_send = true

async function send_command_to_server(operation) {
    if (!allow_command_send) return
    allow_command_send = false

    const server_list = [...document.querySelectorAll("tr:has(td:first-child input[type=checkbox]:checked)")].map(tr => tr.getAttribute("server_name"));
    console.log(server_list)

    let resp = (await fetch(`/manage/${operation}`, {
        method: "POST",
        body: JSON.stringify({'server_list': server_list}),
        headers: {'Content-Type': 'application/json'}
    }))
    resp = await resp.json()
    console.log(resp)

    switch (resp['code']){
        case 'ok':
            alert(`Operacja ${operation} na: ${server_list} przebiegła pomyślnie.`)
            break
        case 'wrong_screen_name':
            alert("Nie znaleziono screena. Sprawdź konsolę przeglądarki.")
            break
        default:
            alert(`Nie rozpoznano kodu: ${resp['code']}`)
    }

    clear_displayed_servers()
    get_servers()

    allow_command_send = true
}

function clear_displayed_servers() {
    document.querySelector("#servers_table tbody").innerHTML = ""
}

document.querySelector(".controls>.buttons").addEventListener('click', (ev) => {
    const operation = ev.target.getAttribute("operation")
    send_command_to_server(operation)
})

window.onload = get_servers()


