import React from 'react';

const ProductTable = ({ products }) => {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <thead>
          <tr style={{ backgroundColor: '#f8f9fa', borderBottom: '2px solid #dee2e6', textAlign: 'left' }}>
            <th style={{ padding: '12px' }}>SKU</th>
            <th style={{ padding: '12px' }}>Nombre</th>
            <th style={{ padding: '12px' }}>Categoría</th>
            <th style={{ padding: '12px' }}>Precio Venta</th>
            <th style={{ padding: '12px' }}>Stock Actual</th>
          </tr>
        </thead>
        <tbody>
          {products.length === 0 ? (
            <tr>
              <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#6c757d' }}>
                No se encontraron productos que coincidan con la búsqueda.
              </td>
            </tr>
          ) : (
            products.map((product) => {
              const stock = product.stock || 0;
              const isLowStock = stock <= 5;
              const price = Number(product.price || product.precio || 0);

              return (
                <tr key={product._id || product.id || product.sku} style={{ borderBottom: '1px solid #e9ecef' }}>
                  <td style={{ padding: '12px', fontWeight: 'bold', color: '#495057' }}>{product.sku}</td>
                  <td style={{ padding: '12px' }}>{product.name || product.nombre}</td>
                  <td style={{ padding: '12px' }}>
                    <span style={{ background: '#e9ecef', padding: '4px 8px', borderRadius: '4px', fontSize: '0.85rem' }}>
                      {product.category || product.categoria || 'Sin Categoría'}
                    </span>
                  </td>
                  <td style={{ padding: '12px', color: '#28a745', fontWeight: 'bold' }}>
                    ${price.toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                  </td>
                  <td style={{ padding: '12px' }}>
                    <span
                      style={{
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontWeight: 'bold',
                        fontSize: '0.85rem',
                        color: '#fff',
                        backgroundColor: isLowStock ? '#dc3545' : '#198754',
                      }}
                    >
                      {stock} u.
                    </span>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ProductTable;
