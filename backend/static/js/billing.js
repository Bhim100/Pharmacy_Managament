let customerMode = "existing";
let medicineCatalog = [];

function getBatchListForMedicine(medicineName) {
    const selectedMedicine = medicineCatalog.find((medicine) => medicine.name === medicineName);
    return selectedMedicine ? selectedMedicine.batches : [];
}

function updateBatchOptions(medicineSelect) {
    const row = medicineSelect.closest(".bill-item-row");
    const batchSelect = row.querySelector(".bill-item-batch");
    const batches = getBatchListForMedicine(medicineSelect.value);

    // The batch dropdown depends on the selected medicine so invalid batch choices are avoided.
    batchSelect.innerHTML = '<option value="">Select Batch</option>';

    batches.forEach((batch) => {
        const option = document.createElement("option");
        option.value = batch;
        option.textContent = batch;
        batchSelect.appendChild(option);
    });
}

function setCustomerMode(mode) {
    customerMode = mode;

    const customerIdField = document.getElementById("customerIdField");
    const customerNameField = document.getElementById("customerNameField");
    const customerPhoneField = document.getElementById("customerPhoneField");
    const modeButtons = document.querySelectorAll(".mode-btn");

    // The form switches fields based on whether the bill is for a saved or walk-in customer.
    if (mode === "existing") {
        customerIdField.classList.remove("is-hidden");
        customerNameField.classList.add("is-hidden");
        customerPhoneField.classList.add("is-hidden");
    } else {
        customerIdField.classList.add("is-hidden");
        customerNameField.classList.remove("is-hidden");
        customerPhoneField.classList.remove("is-hidden");
    }

    modeButtons.forEach((button) => {
        button.classList.toggle("active", button.dataset.mode === mode);
    });
}

function previewBill() {
    const preview = document.getElementById("billPreview");
    const customerIdField = document.getElementById("customerIdField");
    const customerNameField = document.getElementById("customerNameField");
    const customerPhoneField = document.getElementById("customerPhoneField");
    const billItemRows = document.querySelectorAll(".bill-item-row");

    // The preview text changes so the user can confirm which customer flow is being used.
    const customerLabel = customerMode === "existing"
        ? `Existing Customer ID: ${customerIdField.value || "C-2001"}`
        : `New Customer: ${customerNameField.value || "Walk-in Customer"} (${customerPhoneField.value || "No phone added"})`;

    const previewItems = [];
    let totalQuantity = 0;

    // Each visible bill row contributes one preview line so multiple medicines can be reviewed together.
    billItemRows.forEach((row, index) => {
        const medicineName = row.querySelector(".bill-item-name").value || `Medicine ${index + 1}`;
        const batchNo = row.querySelector(".bill-item-batch").value || "Batch not selected";
        const quantity = Number(row.querySelector(".bill-item-qty").value || 1);

        totalQuantity += quantity;
        previewItems.push(`
            <li>
                <strong>${medicineName}</strong> | Batch: ${batchNo} | Qty: ${quantity}
            </li>
        `);
    });

    preview.innerHTML = `
        <div class="preview-header">
            <div>
                <p class="preview-label">Bill ID</p>
                <strong>B-1024</strong>
            </div>
            <div>
                <p class="preview-label">Customer</p>
                <strong>${customerLabel}</strong>
            </div>
        </div>
        <div class="preview-section">
            <p class="preview-label">Items</p>
            <ul class="preview-item-list">${previewItems.join("")}</ul>
        </div>
        <div class="preview-summary">
            <div><span>Total Quantity</span><strong>${totalQuantity}</strong></div>
            <div><span>Discount</span><strong>Rs. 5</strong></div>
            <div><span>Total</span><strong>Rs. 55</strong></div>
        </div>
    `;
}

function addBillItem() {
    const container = document.getElementById("billItemsContainer");

    // New item rows let one bill contain multiple medicines before backend billing is wired in.
    const row = document.createElement("div");
    row.className = "bill-item-row";
    row.innerHTML = `
        <select class="bill-item-name" onchange="updateBatchOptions(this)">
            <option value="">Select Medicine</option>
            ${medicineCatalog.map((medicine) => `<option value="${medicine.name}">${medicine.name}</option>`).join("")}
        </select>
        <select class="bill-item-batch">
            <option value="">Select Batch</option>
        </select>
        <input type="number" class="bill-item-qty" min="1" placeholder="Quantity">
    `;

    container.appendChild(row);
}

function removeLastBillItem() {
    const container = document.getElementById("billItemsContainer");
    const rows = container.querySelectorAll(".bill-item-row");

    // Keep at least one row available so the billing form never becomes empty.
    if (rows.length === 1) {
        rows[0].querySelector(".bill-item-name").value = "";
        rows[0].querySelector(".bill-item-batch").innerHTML = '<option value="">Select Batch</option>';
        rows[0].querySelector(".bill-item-qty").value = "";
        return;
    }

    rows[rows.length - 1].remove();
}

document.addEventListener("DOMContentLoaded", () => {
    const medicineDataElement = document.getElementById("billingMedicineData");
    if (medicineDataElement) {
        // The template injects billing dropdown data once so JS can reuse it for new rows.
        medicineCatalog = JSON.parse(medicineDataElement.textContent);
    }
    setCustomerMode("existing");
});
