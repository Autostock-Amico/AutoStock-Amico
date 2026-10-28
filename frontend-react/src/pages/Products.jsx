import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import ProductTable from '../components/ProductTable';

const Products = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError('');
      try {
        const response = await axiosClient.get('/products');
        const data = Array.isArray(response.data) ? response.data : (response.data.products || []);
        setProducts(data);
      } catch (err) {
        // Mock fallback para pruebas locales
        setProducts([
          { id: '1', sku: 'FLT-001', name: 'Filtro de Aceite', category: 'Filtros', price: 4500, stock: 12 },
          { id: '2', sku: 'FLT-002', name: 'Filtro de Aire', category: 'Filtros', price: 6200, stock: 3 },
          { id: '3', sku: 'ACE-010', name: 'Aceite Sintético 5W30', category: 'Lubricantes', price: 28500, stock: 8 },
          { id: '4', sku: 'PST-005', name: 'Pastillas de Freno Delanteras', category: 'Frenos', price: 18900, stock: 2 }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const categories = useMemo(() => {
    const cats = products.map((p) => p.category || p.categoria).filter(Boolean);
    return [...new Set(cats)];
  }, [products]);

  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      const name = (product.name || product.nombre || '').toLowerCase();
      const sku = (product.sku || '').toLowerCase();
      const query = searchQuery.toLowerCase();

      const matchesSearch = name.includes(query) || sku.includes(query);
      const matchesCategory = !selectedCategory || (product.category || product.categoria) === selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }, [products, searchQuery, selectedCategory]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ color: '#333', margin: 0 }}>Catálogo de Productos (React)</h1>
        <button
          onClick={handleLogout}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#dc3545',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold',
          }}
        >
          Cerrar Sesión
        </button>
      </div>

      {/* Filtros de Búsqueda */}
      <div
        style={{
          display: 'flex',
          gap: '1rem',
          marginBottom: '1.5rem',
          background: '#fff',
          padding: '1rem',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
        }}
      >
        <div style={{ flex: 2 }}>
          <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.9rem', fontWeight: 'bold' }}>
            Buscar (SKU / Nombre)
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Ej: ART-001 o Aceite..."
            style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box', border: '1px solid #ced4da', borderRadius: '4px' }}
          />
        </div>

        <div style={{ flex: 1 }}>
          <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.9rem', fontWeight: 'bold' }}>
            Categoría
          </label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{
              width: '100%',
              padding: '0.5rem',
              boxSizing: 'border-box',
              border: '1px solid #ced4da',
              borderRadius: '4px',
              background: 'white',
            }}
          >
            <option value="">Todas las categorías</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Estado Carga / Tabla */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#007bff', fontWeight: 'bold' }}>
          Cargando catálogo...
        </div>
      ) : error ? (
        <div style={{ color: '#721c24', backgroundColor: '#f8d7da', padding: '1rem', borderRadius: '4px', marginBottom: '1rem' }}>
          {error}
        </div>
      ) : (
        <ProductTable products={filteredProducts} />
      )}
    </div>
  );
};

export default Products;
