const bill = [{
        name: "Pepsi",
        amount: 1,
        price: 1.90
    },
    {
        name: "Hamburger",
        amount: 2,
        price: 7.90
    },
    {
        name: "Fries",
        amount: 1,
        price: 4.90
    },
    {
        name: "Beer",
        amount: 3,
        price: 2.90
    },
    {
        name: "Apple",
        amount: 2,
        price: 1.80
    },
    {
        name: "Coke",
        amount: 1,
        price: 8.90
    },
]

function createBillingList() {
    const parentNode = document.getElementById("billItems")
    parentNode.innerHTML = ""

    let total = 0

    for (const item of bill) {
        total += item.amount * item.price

        const itemBox = document.createElement("div")
        itemBox.setAttribute("class", "item-box")
        itemBox.setAttribute("id", `item-box-id-${bill.indexOf(item)}`)
        itemBox.setAttribute("draggable", "true")
        itemBox.addEventListener("dragstart", onDragStart)
        itemBox.addEventListener("dragend", onDragEnd)

        const itemNameBox = document.createElement("div")
        itemNameBox.setAttribute("class", "itemName-box")
        itemNameBox.innerHTML = item.name
        itemBox.appendChild(itemNameBox)

        const itemCalcBox = document.createElement("div")
        itemCalcBox.setAttribute("class", "itemCalc-box")
        itemCalcBox.innerHTML = `${item.amount} x £${(item.price).toFixed(2)}`
        itemBox.appendChild(itemCalcBox)

        const itemTotalBox = document.createElement("div")
        itemTotalBox.setAttribute("class", "itemTotal-box")
        itemTotalBox.innerHTML = `£${(item.amount * item.price).toFixed(2)}`
        itemBox.appendChild(itemTotalBox)

        parentNode.appendChild(itemBox)
    }

    document.getElementById("billSum").innerHTML = `£${(total).toFixed(2)} `
}

createBillingList()

function handleSelectChange() {
    const memberAmount = parseInt(document.getElementById("party-members-amount").value)
    const parentNode = document.getElementById("party-members")
    parentNode.innerHTML = ""

    for (let i = 0; i < memberAmount; i++) {
        const memberBox = document.createElement("div")
        memberBox.setAttribute("class", "member-box")
        memberBox.setAttribute("dropzone", "true")
        memberBox.addEventListener("dragover", (event) => event.preventDefault())
        memberBox.addEventListener("dragenter", onDragEnter)
        memberBox.addEventListener("dragleave", onDragLeave)
        memberBox.addEventListener("drop", onDrop)
        parentNode.appendChild(memberBox)
    }
}

handleSelectChange()

let draggedId = ""

function onDragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.id)
    draggedId = event.target.id
    document.getElementById(event.target.id).classList.add("dragging")
    console.log("start", draggedId)
}

function onDragEnd(event) {
    document.getElementById(event.target.id).classList.remove("dragging")
    console.log("end", draggedId)
    event.preventDefault()
}

function onDragEnter(event) {
    console.log("enter", draggedId)
    event.preventDefault()
}

function onDragLeave(event) {
    console.log("leave", draggedId)
    event.preventDefault()
}

function onDrop(event) {
    const id = draggedId
    console.log("drop", id)
    event.preventDefault()
}