window.onload = async () => {
    // pobranie statusow serwerow mc
    try {
        var resp = await fetch("/getServerStatus/all")
        resp = await resp.json()
    } catch (e) {
        console.error(`Podczas proby pobrania statusow serwerow, wystapil blad: ${e}`)
    }

    Object.entries(resp).forEach(data => {
        const server_name = data[0]
        const server_ping = data[1]
        change_server_status(server_name, server_ping)
    })
    console.log(resp)


    // przypisanie funkcji do przyciskow
    const server_control_buttons = document.querySelectorAll(".server_item button")
    server_control_buttons.forEach((button) => {
        console.log(button)
        try {
            bind_function_to_button(button)
        } catch (e){
            console.error(`Nie mozna przypisac funkcji do przycisku ${button}: ${e}`)
        }
    })

}

function bind_function_to_button(button) {
    const server_item = button.closest(".server_item")
    const server_name = server_item.getAttribute("server_name")
    const button_function = button.classList.value
    console.log(button_function)

    if (button_function === 'terminal') {
        console.log(`przypisuje terminal dla serwera ${server_name}`)
    } else {
        button.addEventListener('click', () => {
            manage_server(server_name, button_function)
        })
    }

}

async function manage_server(server_name, operation) {
    let resp = await fetch(`/manage/${server_name}/${operation}`, {method: "POST"})

    if (resp.status === 200) {
        alert(`[OK] Operacja ${operation} na serwerze ${server_name} powiodla sie.`)
    } else {
        alert(`[NIE OK] Operacja ${operation} na serwerze ${server_name} NIE powiodla sie.`)
    }
}


function change_server_status(server_name, server_ping) {
    let status = 'on'

    if (server_ping < 0) {
        status = 'off'
    }


    document.getElementById(`${server_name}_status`).classList.value = `state_display ${status}`
}


