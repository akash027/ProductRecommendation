document.addEventListener("DOMContentLoaded", () => {
    const categoryForm = document.getElementById("category-form");
    const categorySelect = document.getElementById("category");
    const productSelect = document.getElementById("product");
    const productDetailsDiv = document.getElementById("product-details");
    const getRecommendationsButton = document.getElementById("get-recommendations");
    const recommendationsDiv = document.getElementById("recommendations");

    // Fetch products when a category is selected
    categoryForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const selectedCategory = categorySelect.value;

        fetch("/filter", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `category=${encodeURIComponent(selectedCategory)}`,
        })
            .then((response) => response.json())
            .then((products) => {
                productSelect.innerHTML = '<option value="" disabled selected>Select a product</option>';
                products.forEach((product) => {
                    const option = document.createElement("option");
                    option.value = product.product_name;
                    option.textContent = product.product_name;
                    productSelect.appendChild(option);
                });
                productDetailsDiv.innerHTML = "";
                recommendationsDiv.innerHTML = "";
                getRecommendationsButton.disabled = true;
            });
    });

    // Fetch product details when a product is selected
    productSelect.addEventListener("change", () => {
        const selectedProduct = productSelect.value;

        fetch("/details", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `product_name=${encodeURIComponent(selectedProduct)}`,
        })
            .then((response) => response.json())
            .then((details) => {
                productDetailsDiv.innerHTML = `
                    <div class="card">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img src="${details.img_link}" class="product-image" alt="${details.product_name}">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">${details.product_name}</h5>
                                    <p class="card-text"><strong>Category:</strong> ${details.category}</p>
                                    <p class="card-text"><strong>Rating:</strong> ${details.rating} (${details.rating_count} reviews)</p>
                                    <a href="${details.product_link}" target="_blank" class="btn btn-primary">View Product</a>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                getRecommendationsButton.disabled = false;
            });
    });

    // Fetch recommendations when the button is clicked
    getRecommendationsButton.addEventListener("click", () => {
        const selectedProduct = productSelect.value;

        fetch("/recommendations", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `product_name=${encodeURIComponent(selectedProduct)}`,
        })
            .then((response) => response.json())
            .then((recommendations) => {
                recommendationsDiv.innerHTML = "";
                recommendations.forEach((rec, index) => {
                    recommendationsDiv.innerHTML += `
                        <div class="col-md-4">
                            <div class="card recommendation-card">
                                <img src="${rec.img_link}" class="card-img-top" alt="${rec.product_name}">
                                <div class="card-body">
                                    <h5 class="card-title">${rec.product_name}</h5>
                                    <p class="card-text"><strong>Category:</strong> ${rec.category}</p>
                                    <p class="card-text"><strong>Rating:</strong> ${rec.rating} (${rec.rating_count} reviews)</p>
                                    <a href="${rec.product_link}" target="_blank" class="btn btn-success">View Product</a>
                                </div>
                            </div>
                        </div>
                    `;
                });
            });
    });
});
