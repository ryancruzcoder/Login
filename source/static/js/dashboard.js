const billing = document.querySelector(".money").value;

const ctx = document.getElementById("myChart").getContext("2d");

const gradient = ctx.createLinearGradient(0, 0, 0, 400);

gradient.addColorStop(0, "#5cffca")

gradient.addColorStop(1, "#66ff")

const labels = [

    "10/05",
    "11/05",
    "12/05",
    "13/05",
    "14/05",
    "15/05",
    "16/05"

];

const data = {

    labels,
    datasets: [{
        data:[50, 100, 200, 60, 400, 460, billing],
        label: "Weekly",
        fill: true,
        backgroundColor: gradient
        
    }]
};

const config = {
    type: "line",
    data,
    options: {
        responsive: true
    }
};

const myChart = new Chart(ctx, config);

const BtnAdd = document.querySelector(".btn.add.sale");
const BtnDrop = document.querySelector(".btn.drop.sale");
const modal = document.querySelector("dialog.modal");
const modalDrop = document.querySelector("dialog.modal.drop");
const modalBtnClose = document.querySelector(".btn.modal.close");
const modalBtnCloseDrop = document.querySelector(".btn.modal.close.drop");

BtnAdd.onclick = function() {
    modal.showModal();
};

BtnDrop.onclick = function() {
    modalDrop.showModal();
};

modalBtnClose.onclick = function() {
    modal.close();
};

modalBtnCloseDrop.onclick = function() {
    modalDrop.close();
};

const BtnAddProduct = document.querySelector("input.btn.addproduct");
const BtnDropProduct = document.querySelector("input.btn.drop.product");
const BtnCloseModalAddProduct = document.querySelector(".btn.modal.close.drop.product");
const BtnCloseModalDropProduct = document.querySelector(".btn.modal.close.drop");
const modalAddProduct = document.querySelector(".modal.product.add");
const modalDropProduct = document.querySelector(".modal.drop.product.dois");

BtnAddProduct.onclick = function() {
    modalAddProduct.showModal()
}

BtnCloseModalAddProduct.onclick = function() {
    modalAddProduct.close()
}

BtnDropProduct.onclick = function() {
    modalDropProduct.showModal()
}

BtnCloseModalDropProduct.onclick = function() {
    modalDropProduct.close()
}



