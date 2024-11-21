/**
 * Este JS es para el manejo de filtros dentro de la tabla productos
 */

let dataTable;
let dataTableEsIniciada = false;

/*Aqui se ponen las opciones de la tabla en este caso
className es un estilo del css
orderable si X objeto se puede ordenar o no 
searchable si X objeto se puede buscar*/ 

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4] }, // esto centra los datos segun el css
        { orderable: false, targets: [0, 1, 4] }, // no se pueden ordenar las columnas 1, 2 y 5 de la tabla
        { searchable: false, targets: [0, 2, 3, 4] }, // no se pueden buscar las columnas 1, 3, 4 y 5 de la tabla
    ],
    destroy: true
};

/**
 * Inicializa la tabla
 * destruye alguna tabla existente en caso de que se agreguen nuevas cosas
 * espera a que listaProducto consiga los datos 
 * crea la datatable consiguiendo el ID de la tabla creada en HTML
 * y cambia el valor de es inicializada a true
 */
const initDataTable = async () => {
    if (dataTableEsIniciada) {
        dataTable.destroy();
    }
    await listaProducto();
    dataTable = $('#datatable-productos').DataTable(dataTableOptions); // Aqui se crea lo que es la DATATABLE
    dataTableEsIniciada = true;
};

/**
 * Consigue los datos para pasarlos a la tabla
 * en este caso hace un fetch de una url creada por nosotros
 * que consigue los datos de la BD y los pasa a un JSON
 * luego crea por cada dato las rows de la tabla
 */
const listaProducto = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/inventario/deshabilitados/lista/');
        const data = await response.json();
        console.log(data); 
        let content = '';
        data.productos.forEach((producto, index) => {
            const habilitarUrl = habilitarUrlTemplate.replace("0", producto.id);
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${producto.nombre}</td>
                    <td>${producto.cantidad}</td>
                    <td>${producto.precio}</td>
                    <td>
                        <!-- Botón para deshabilitar, redirige a la vista de deshabilitación con confirmación -->
                        <a href="${habilitarUrl}" class='btn btn-success' onclick="return confirm('¿Estás seguro de Habilitar este producto?');">
                            <i class="bi bi-check-circle"></i>
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

// esto creo que era para saber si cargó la tabla/página de la tabla
window.addEventListener('load', async () => {
    await initDataTable();
});
