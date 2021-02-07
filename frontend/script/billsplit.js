//#region datainput
// const receiptName = "KFC"
//
// const bill = [
//     { name: "Pepsi", quantity: 1, price: 1.90 },
//     { name: "Hamburger", quantity: 2, price: 7.90 },
//     { name: "Fries", quantity: 1, price: 4.90 },
//     { name: "Beer", quantity: 3, price: 2.90 },
//     { name: "Apple", quantity: 2, price: 1.80 },
//     { name: "Coke", quantity: 1, price: 8.90 },
// ]

let receiptName = "";
let bill = [];
//#endregion

function getData(){
    bill = localStorage.getItem('data')
    genSerialBill()
    updateBillingLists()
}

//#region class declaration
class BillItem {
    constructor(name, quantity, price) {
        this.name = name
        this.quantity = quantity
        this.price = price
        this.needsUpdate = true
    }

    getCopy(empty = false) {
        if (empty)
            return new BillItem(this.name, 0, this.price)
        else
            return new BillItem(this.name, this.quantity, this.price)
    }

    getHTML(id, draggable = false) {
        const itemBox = document.createElement("div")
        {
            itemBox.classList.add("itembox")
            itemBox.classList.add("half-round-box")
            itemBox.classList.add("reversed-half-round-box")
            
            itemBox.setAttribute("id", id)
            if (draggable) {
                itemBox.setAttribute("draggable", "true")
                itemBox.addEventListener("dragstart", onDragStart)
                itemBox.addEventListener("dragend", onDragEnd)
            } else {
                itemBox.classList.add("itemboxselected")
                itemBox.addEventListener("mouseup", onMouseUp)
            }
        }

        {
            const itemNameBox = document.createElement("div")
            itemNameBox.setAttribute("class", "itemName-box")
            itemNameBox.innerHTML = this.name
            itemBox.appendChild(itemNameBox)

            const itemCalcBox = document.createElement("div")
            itemCalcBox.setAttribute("class", "itemCalc-box")
            itemCalcBox.innerHTML = `${this.quantity} x £${(this.price).toFixed(2)}`
            itemBox.appendChild(itemCalcBox)

            const itemTotalBox = document.createElement("div")
            itemTotalBox.setAttribute("class", "itemTotal-box")
            itemTotalBox.innerHTML = `£${(this.quantity * this.price).toFixed(2)}`
            itemBox.appendChild(itemTotalBox)
        }

        return itemBox
    }
}
//#endregion

let serializedBill = {}
function genSerialBill()
{
    for (let i = 0; i < bill.length; i++) {
        const item = bill[i]
        serializedBill[i] = Object.freeze(new BillItem(item.name, item.quantity, item.price))
    }
}
Object.freeze(serializedBill)

const openBill = {}
Object.keys(serializedBill).forEach(itemId => {
    openBill[itemId] = serializedBill[itemId].getCopy()
})

const memberBills = {}
//#endregion

//#region javascript logic
function updateBillingLists() {
    {
        const parentNode = document.getElementById("items")
        parentNode.innerHTML = ""

        Object.keys(openBill).forEach(itemId => {
            const item = openBill[itemId]
            if (item.needsUpdate && item.quantity > 0) {
                parentNode.appendChild(item.getHTML(`op-${itemId}`, true))
            }
        })
    }

    {
        const parentNode = document.getElementById("party-members")
        Object.keys(memberBills).forEach(memberName => {
            const member = memberBills[memberName]
            console.log(member)
            if (!member.init) {
                member.init = true
                const memberBox = document.createElement("div")
                memberBox.setAttribute("class", "sharesbox")
                memberBox.classList.add("half-round-box")
                memberBox.setAttribute("id", `mb-${memberName}`)
                memberBox.setAttribute("dropzone", "true")
                memberBox.addEventListener("dragover", (event) => event.preventDefault())

                memberBox.addEventListener("drop", onDrop)

                const memberNameBox = document.createElement("div")
                memberNameBox.classList.add("sharesboxtitle")
                memberNameBox.classList.add("half-round-box")
                memberNameBox.innerHTML = memberName

                memberBox.appendChild(memberNameBox)

                parentNode.appendChild(memberBox)
            }

            Object.keys(member.list).forEach(billItemId => {
                const billItem = member.list[billItemId]
                if (billItem.needsUpdate) {
                    if (billItem.quantity > 0) {
                        const node = document.getElementById(`mb-${memberName}-${billItemId}`)
                        if (node) {
                            node.replaceWith(billItem.getHTML(`mb-${memberName}-${billItemId}`))
                        } else {
                            document.getElementById(`mb-${memberName}`).appendChild(billItem.getHTML(`mb-${memberName}-${billItemId}`))
                        }
                    } else {
                        const node = document.getElementById(`mb-${memberName}-${billItemId}`)
                        if (node)
                            node.remove()
                    }
                }
            })
        })
    }

    {
        const parentNode = document.getElementById("summary")
        parentNode.innerHTML = ""
        Object.keys(memberBills).forEach(memberId => {
            const member = memberBills[memberId]
            const billingBox = document.createElement("div")
            billingBox.classList.add("half-round-box")
            billingBox.classList.add("summarybox")

            {
                const billingBoxName = document.createElement("input")
                billingBoxName.classList.add("half-round-box")
                billingBoxName.id = `input-${memberId}`
                billingBoxName.addEventListener("keydown", onKeydown)
                billingBoxName.value = memberId
                billingBox.appendChild(billingBoxName)
            }

            {
                let totalPrice = 0
                Object.keys(member.list).forEach(itemId => {
                    totalPrice += member.list[itemId].price * member.list[itemId].quantity 
                })
                const billingBoxTotal = document.createElement("div")
                billingBoxTotal.classList.add("right")
                billingBoxTotal.innerHTML = "£" + totalPrice.toFixed(2)
                billingBox.appendChild(billingBoxTotal)
            }

            parentNode.appendChild(billingBox)
        })
        const billingBox = document.createElement("div")
        billingBox.classList.add("half-round-box")
        billingBox.classList.add("summarybox")
        billingBox.classList.add("openbill")

        {
            const billingBoxName = document.createElement("div")
            billingBoxName.classList.add("left")
            billingBoxName.innerHTML = "Open bill"
            billingBox.appendChild(billingBoxName)
        }

        {
            let totalPrice = 0
            Object.keys(openBill).forEach(itemId => {
                totalPrice += openBill[itemId].price * openBill[itemId].quantity
            })
            const billingBoxTotal = document.createElement("div")
            billingBoxTotal.classList.add("right")
            billingBoxTotal.innerHTML = "£" + totalPrice.toFixed(2)
            billingBox.appendChild(billingBoxTotal)
        }

        parentNode.appendChild(billingBox)
    }

}

let supportedNames = ["Dog", "Cat", "Bird", "Fish", "Monkey", "Eagle", "Turtle", "Duck"]

function getRandomAnimal() {
    const animal = supportedNames.pop()
    console.log(animal)
    return animal
}

let lastMemberAmount = 0

function handleSelectChange() {
    const memberAmount = parseInt(document.getElementById("party-members-amount").value)

    if (Object.keys(memberBills).length > memberAmount) {
        if (window.confirm("There are items in your basket! Selecting a lower number of members will reset your bill. Do you wish to continue?")) {
            location.reload()
        } else {
            document.getElementById("party-members-amount").value = lastMemberAmount
            return
        }
    }
    lastMemberAmount = memberAmount


    while (Object.keys(memberBills).length < memberAmount) {
        memberBills[getRandomAnimal()] = {
            init: false,
            needsUpdate: true,
            list: {}
        }
    }
    console.log(memberBills)
    updateBillingLists()
}

handleSelectChange()
//#endregion

//#region dragevents
let draggedId = ""
let entered = undefined
let dragging = false

function onDragStart(event) {

    dragging = true

    event.dataTransfer.setData('text/plain', event.currentTarget.id)
    draggedId = event.currentTarget.id


    document.getElementById(event.currentTarget.id).classList.add("dragging")

    console.log("start", draggedId)
}

function onDragEnd(event) {
    dragging = false
    const element = document.getElementById(event.currentTarget.id)
    if (element)
        element.classList.remove("dragging")

    console.log("end", draggedId)
    event.preventDefault()
}

function onDrop(event) {
    if (dragging) {
        const itemId = draggedId.replace("op-", "")
        const memberId = event.currentTarget.id.replace("mb-", "")

        const member = memberBills[memberId]

        const billItem = openBill[itemId]
        billItem.amount--
        billItem.needsUpdate = true

        console.log(itemId, member, member, billItem)

        if (member.list[itemId]) {
            member.list[itemId].needsUpdate = true
            member.list[itemId].quantity++

        } else {
            const copiedBillItem = billItem.getCopy(true)
            copiedBillItem.quantity++
            member.list[itemId] = copiedBillItem
        }

        updateBillingLists()

        console.log("drop", event.currentTarget.id)

        const id = draggedId
        console.log("drop", id)
        event.preventDefault()
    }
}

function onMouseUp(event) {
    console.log(event.currentTarget.id)
    const [_, memberId, itemId] = event.currentTarget.id.split("-")

    console.log(_, memberId, itemId)

    const member = memberBills[memberId]
    const billItem = openBill[itemId]
    const memberBillItem = member.list[itemId]

    billItem.quantity++
    billItem.needsUpdate = true

    memberBillItem.quantity--
    billItem.needsUpdate = true

    updateBillingLists()
}
//#endregion

function onKeydown(event) {
    if (event.key === "Enter") {
        const inputNode = document.getElementById(event.currentTarget.id)
        const changedName = inputNode.value

        const previousName = inputNode.id.replace("input-", "")

        if (memberBills[changedName] !== undefined) {
            inputNode.value = previousName
            window.alert("Names have to unique!")
        } else {
            document.getElementById(`mb-${previousName}`).remove()

            memberBills[changedName] = memberBills[previousName]
            memberBills[changedName].init = false

            delete memberBills[previousName]

            updateBillingLists()
        }
    }
}

function roundTwo(number) {
    return Math.round(number * 100) / 100
}

function onSubmit() {

    if (!window.confirm("Are you sure you want to submit? The page will be reset!"))
        return

    let receiptTotal = 0
    for (const billItem of bill) {
        receiptTotal += billItem.price * billItem.quantity
    }
    const outputSplits = []
    Object.keys(memberBills).forEach(memberId => {
        const member = memberBills[memberId]
        let memberTotal = 0
        const memberItems = []
        Object.keys(member.list).forEach(itemId => {
            const item = member.list[itemId]
            memberTotal += item.price * item.quantity
            memberItems.push({
                name: item.name,
                price: item.price,
                quantity: item.quantity
            })
        })
        outputSplits.push({
            name: memberId,
            total: roundTwo(memberTotal),
            items: memberItems
        })
    })
    const output = {
        receipt: {
            name: receiptName,
            total: roundTwo(receiptTotal),
            items: bill
        },
        splits: outputSplits
    }
    console.log(JSON.stringify(output, null, 4))
    location.reload()
    // fetch("localhost:5000/save", {method: "POST", body: JSON.stringify(output)}).then(result => {
    //     if (result.status === 200) {
    //         window.alert("Successfully submitted data")
    //         location.reload()
    //     } else {
    //         window.alert(`Failed submitting data: ${result.status} | ${result.statusText}`)
    //     }
    // })
}