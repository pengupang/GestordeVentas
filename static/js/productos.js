/**
 * Este JS es para el manejo de filtros dentro de la tabla productos
 */

let dataTable;
let dataTableEsIniciada = false;

/* Opciones de configuración para la DataTable */
const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4] },
        { orderable: false, targets: [0, 1, 4] },
        { searchable: false, targets: [0, 2, 3, 4] },
    ],
    destroy: true
};

// Umbral de stock bajo
const umbralStock = 10;

// Función para verificar el stock bajo
const verificarStockBajo = () => {
    let hayBajoStock = false;

    const celdasStock = document.querySelectorAll('.cantidad');
    celdasStock.forEach(celda => {
        const cantidad = parseInt(celda.textContent.trim());
        if (cantidad < umbralStock) {
            hayBajoStock = true;

            const fila = celda.closest('tr');
            if (fila) {
                fila.classList.add('bg-danger', 'text-white');
                fila.title = '¡Bajo stock!';
            }
        }
    });

    const alerta = document.getElementById('alerta-stock-bajo');
    if (hayBajoStock) {
        alerta.classList.remove('d-none');
    } else {
        alerta.classList.add('d-none');
    }
};

// Inicializar DataTable y verificar stock después de renderizar
document.addEventListener('DOMContentLoaded', function () {
    if (typeof $ === "undefined") {
        console.error("Error: jQuery no está cargado. Verifica la inclusión de la biblioteca.");
        return;
    }

    $(document).ready(async function () {
        await initDataTable();

        // Ejecutar la verificación de stock bajo después de cada renderizado
        $('#datatable-productos').on('draw.dt', function () {
            verificarStockBajo();
        });

        // Verificar stock bajo al cargar inicialmente la tabla
        verificarStockBajo();
    });
});

/**
 * Inicializa la tabla
 */
const initDataTable = async () => {
    if (dataTableEsIniciada) {
        dataTable.destroy();
    }
    await listaProducto();
    dataTable = $('#datatable-productos').DataTable(dataTableOptions);
    dataTableEsIniciada = true;
};

/**
 * Consigue los datos para pasarlos a la tabla
 */
const listaProducto = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/inventario/lista/');
        const data = await response.json();
        console.log(data);
        let content = '';
        data.productos.forEach((producto, index) => {
            const deshabilitarUrl = deshabilitarUrlTemplate.replace("0", producto.id);
            const actualizarUrl = actualizarUrlTemplate.replace("0", producto.id);
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${producto.nombre}</td>
                    <td class="cantidad">${producto.cantidad}</td>
                    <td>${producto.precio}</td>
                    <td>
                        <a href="${actualizarUrl}" class='btn btn-warning'>
                            <i class="bi bi-pencil"></i>
                        </a>
                        <a href="${deshabilitarUrl}" class='btn btn-danger' onclick="return confirm('¿Estás seguro de deshabilitar este producto?');">
                            <i class="bi bi-x-circle"></i>
                        </a>
                    </td>
                </tr>
            `;
        });
        cuerpoTabla_productos.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

// Ejecutar la inicialización cuando la página cargue
window.addEventListener('load', async () => {
    await initDataTable();
});
