// Function to handle editing a product
function editProduct(productId) {
    $.ajax({
        url: `${API_ENDPOINT}/${productId}`,
        type: 'GET',
        success: (data) => {
            // Populate the input fields with the current product data
            $('#productid').val(data.productid);
            $('#productname').val(data.productname);
            $('#category').val(data.category);
            $('#price').val(data.price);
            $('#quantity').val(data.quantity);

            // Replace "Save Product" button with "Save Changes" button
            $('#buttonContainer').html(`
                <input type="submit" id="saveChanges" value="Save Changes">
            `);

            // Add event listener for the new "Save Changes" button
            document.getElementById("saveChanges").addEventListener("click", function() {
                const inputData = {
                    productid: $('#productid').val(),
                    productname: $('#productname').val(),
                    category: $('#category').val(),
                    price: $('#price').val(),
                    quantity: $('#quantity').val()
                };

                $.ajax({
                    url: `${API_ENDPOINT}/${inputData.productid}`,
                    type: 'PUT',
                    data: JSON.stringify(inputData),
                    contentType: 'application/json; charset=utf-8',
                    success: () => {
                        document.getElementById("productSaved").textContent = "Product Data Updated!";
                        // Clear the input fields after update
                        $('#productid').val(""); 
                        $('#productname').val("");
                        $('#category').val("");
                        $('#price').val("");
                        $('#quantity').val("");
                        getProducts(); // Refresh the product list

                        // Restore "Save Product" button
                        $('#buttonContainer').html(`
                            <input type="submit" id="saveProduct" value="Save Product">
                        `);
                    },
                    error: () => {
                        alert("Error updating product data.");
                    }
                });
            });
        },
        error: () => {
            alert("Error retrieving product data for editing.");
        }
    });
}

// Function to handle saving a new product
document.getElementById("saveProduct").addEventListener("click", function() {
    const inputData = {
        productid: $('#productid').val(),
        productname: $('#productname').val(),
        category: $('#category').val(),
        price: $('#price').val(),
        quantity: $('#quantity').val()
    };

    $.ajax({
        url: API_ENDPOINT,
        type: 'POST',
        data: JSON.stringify(inputData),
        contentType: 'application/json; charset=utf-8',
        success: () => {
            document.getElementById("productSaved").textContent = "Product Data Saved!";
            // Clear the input fields
            $('#productid').val(""); 
            $('#productname').val("");
            $('#category').val("");
            $('#price').val("");
            $('#quantity').val("");
            getProducts(); // Refresh the product list
        },
        error: () => {
            alert("Error saving product data.");
        }
    });
});

// Function to handle retrieving and displaying product data
function getProducts() {
    $.ajax({
        url: API_ENDPOINT,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: (response) => {
            $('#productTable tbody').empty(); // Clear the table body
            response.forEach(data => {
                $("#productTable tbody").append(`
                    <tr>
                        <td>${data.productid}</td>
                        <td>${data.productname}</td>
                        <td>${data.category}</td>
                        <td>${data.price}</td>
                        <td>${data.quantity}</td>
                        <td class="actionButtons" style="white-space: nowrap;">
                            <button onclick="editProduct('${data.productid}')">Edit</button>
                            <button onclick="deleteProduct('${data.productid}')">Delete</button>
                        </td>
                    </tr>
                `);
            });
        },
        error: () => {
            alert("Error retrieving product data.");
        }
    });
}

// Function to handle deleting a product
function deleteProduct(productId) {
    $.ajax({
        url: `${API_ENDPOINT}/${productId}`,
        type: 'DELETE',
        success: () => {
            alert("Product Data Deleted!");
            getProducts(); // Refresh the product list
        },
        error: () => {
            alert("Error deleting product data.");
        }
    });
}
