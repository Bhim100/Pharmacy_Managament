document.addEventListener("DOMContentLoaded", () => {
    const lowStock = [
        "Amoxycillin 500mg - 8 units left",
        "VitaPlus Tablets - 6 units left",
        "Cough Syrup C12 - 4 bottles left"
    ];

    const expiry = [
        "PAR650-B4 expires in 20 days",
        "VIT-25-C2 expires in 15 days",
        "AMX500-A1 expires in 9 days"
    ];

    document.getElementById("lowStockList").innerHTML =
        lowStock.map((item) => `<li>${item}</li>`).join("");

    document.getElementById("expiryList").innerHTML =
        expiry.map((item) => `<li>${item}</li>`).join("");
});
