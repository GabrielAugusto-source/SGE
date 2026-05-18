document.addEventListener('DOMContentLoaded', () => {
    const productForm = document.getElementById('product-form');
    const productTableBody = document.querySelector('#product-table tbody');
    const btnSubmit = document.getElementById('btn-submit');
    const productIdInput = document.getElementById('product-id');

    async function loadProducts() {
        try {
            const response = await fetch('/products/');
            const products = await response.json();
            productTableBody.innerHTML = '';

            products.forEach(prod => {
                const row = `
                    <tr>
                        <td>${prod.id}</td>
                        <td>${prod.name}</td>
                        <td>${prod.quantity}</td>
                        <td>R$ ${prod.price.toFixed(2)}</td>
                        <td>
                            <button class="btn-action btn-edit" onclick="prepareEdit(${JSON.stringify(prod).replace(/"/g, '&quot;')})">✎</button>
                            <button class="btn-action btn-delete" onclick="deleteProduct(${prod.id})">✖</button>
                        </td>
                    </tr>
                `;
                productTableBody.innerHTML += row;
            });
        } catch (error) {
            console.error("Erro ao carregar:", error);
        }
    }

    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = productIdInput.value;
        const data = {
            name: document.getElementById('name').value,
            quantity: parseInt(document.getElementById('quantity').value),
            price: parseFloat(document.getElementById('price').value),
            category_id: parseInt(document.getElementById('category_id').value),
            supplier_id: parseInt(document.getElementById('supplier_id').value),
        };

        try {
            let response;
            if (id) {
                response = await fetch(`/products/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                response = await fetch('/products/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }

            if (response.ok) {
                Swal.fire('Sucesso!', 'Operação realizada com sucesso!', 'success');
                productForm.reset();
                productIdInput.value = '';
                btnSubmit.innerText = 'Salvar Produto';
                loadProducts();
            } else {
                Swal.fire('Erro!', 'Verifique os IDs de Categoria e Fornecedor.', 'error');
            }
        } catch (error) {
            console.error("Erro:", error);
        }
    });

    window.prepareEdit = (product) => {
        document.getElementById('name').value = product.name;
        document.getElementById('quantity').value = product.quantity;
        document.getElementById('price').value = product.price;
        document.getElementById('category_id').value = product.category_id;
        document.getElementById('supplier_id').value = product.supplier_id;
        productIdInput.value = product.id;
        btnSubmit.innerText = 'Atualizar Produto';
        window.scrollTo(0, 0);
    };

    window.deleteProduct = async (id) => {
        Swal.fire({
            title: 'Tem certeza?',
            text: "O produto será removido permanentamente!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sim, deletar!'
        }).then(async (result) => {
            if (result.isConfirmed) {
                const response = await fetch(`/products/${id}`, { method: 'DELETE' });
                if (response.ok) {
                    Swal.fire('Deletado!', 'Produto removido com sucesso.', 'success');
                    loadProducts();
                }
            }
        });
    };

    loadProducts();
});
