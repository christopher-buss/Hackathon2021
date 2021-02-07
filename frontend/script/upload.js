//Image
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

//Jquery
// $(function () {
//     $('#upload').on('change', function () {
//         readURL(input);
//     });
// });

//Preview name
var input = document.getElementById('upload');
var infoArea = document.getElementById('upload-label');

const formData = new FormData();

input.addEventListener('change', showFileName);
function showFileName(event) {
    var input = event.srcElement;
    let file = input.files[0];
    formData.append('photo', file)
    infoArea.textContent = 'File name: ' + file.name;
}

function send() {
    fetch("http://localhost:5000/save_receipt", {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            localStorage.setItem("data", data)
            window.location.href = './pages/billsplit.html'
        })
        .catch(console.error)
}