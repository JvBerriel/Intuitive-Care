<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">🔍 Busca de Operadoras de Saúde</h1>
      <div class="search-container">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          placeholder="Digite nome, CNPJ ou registro ANS..."
          class="search-input"
          aria-label="Campo de busca"
        />
        <button @click="fetchOperadoras" class="search-button" aria-label="Buscar">
          Buscar
        </button>
      </div>
    </header>

    <main class="app-main">
      <div v-if="loading" class="loading-state">
        <div class="spinner" aria-hidden="true"></div>
        <p>Carregando dados...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p role="alert">⚠️ {{ error }}</p>
        <button @click="fetchOperadoras" class="retry-button" aria-label="Tentar novamente">
          Tentar novamente
        </button>
        <p class="support-text" v-if="isCriticalError">
          Se o problema persistir, contate o suporte técnico.
        </p>
      </div>

      <div v-else-if="operadoras.length === 0" class="empty-state">
        <p>Nenhuma operadora encontrada</p>
        <p v-if="searchQuery">para "{{ searchQuery }}"</p>
        <button @click="clearSearch" class="clear-button" v-if="searchQuery">
          Limpar busca
        </button>
      </div>

      <div v-else class="results-container">
        <div class="results-info">
          <span>{{ operadoras.length }} {{ operadoras.length === 1 ? 'resultado' : 'resultados' }}</span>
          <span v-if="searchQuery">para "{{ searchQuery }}"</span>
          <button @click="exportToCSV" class="export-button" v-if="operadoras.length > 0">
            Exportar CSV
          </button>
        </div>

        <div class="table-wrapper">
          <table class="operadoras-table" aria-label="Resultados da busca de operadoras">
            <thead>
              <tr>
                <th 
                  @click="sortBy('razao_social')"
                  :aria-sort="sortColumn === 'razao_social' ? sortDirection : 'none'"
                >
                  Razão Social
                  <span v-if="sortColumn === 'razao_social'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th 
                  @click="sortBy('cnpj')"
                  :aria-sort="sortColumn === 'cnpj' ? sortDirection : 'none'"
                >
                  CNPJ
                  <span v-if="sortColumn === 'cnpj'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th 
                  @click="sortBy('modalidade')"
                  :aria-sort="sortColumn === 'modalidade' ? sortDirection : 'none'"
                >
                  Modalidade
                  <span v-if="sortColumn === 'modalidade'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th>Detalhes</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="op in sortedOperadoras" :key="op.cnpj">
                <td>{{ op.razao_social || 'Não informado' }}</td>
                <td>{{ formatCNPJ(op.cnpj) }}</td>
                <td>{{ op.modalidade || 'Não informado' }}</td>
                <td>
                  <button 
                    @click="showDetails(op)"
                    class="details-button"
                    aria-label="Ver detalhes"
                  >
                    🔍
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <p>Sistema de consulta de operadoras de saúde - ANS {{
currentYear }}</p>
    </footer>

    
    <div v-if="selectedOperadora" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button @click="closeModal" class="modal-close" aria-label="Fechar modal">
          &times;
        </button>
        <h2>{{ selectedOperadora.razao_social }}</h2>
        <div class="modal-details">
          <div v-for="(value, key) in selectedOperadora" :key="key" class="detail-row">
            <span class="detail-label">{{ formatLabel(key) }}:</span>
            <span class="detail-value">{{ value || 'Não informado' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { saveAs } from 'file-saver';

export default {
  data() {
    return {
      searchQuery: '',
      operadoras: [],
      loading: false,
      error: null,
      sortColumn: 'razao_social',
      sortDirection: 'asc',
      debounceTimer: null,
      debounceDelay: 800,
      selectedOperadora: null,
      currentYear: new Date().getFullYear()
    }
  },
  computed: {
    sortedOperadoras() {
      return [...this.operadoras].sort((a, b) => {
        const valA = a[this.sortColumn] || '';
        const valB = b[this.sortColumn] || '';
        
        if (valA < valB) return this.sortDirection === 'asc' ? -1 : 1;
        if (valA > valB) return this.sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    },
    isCriticalError() {
      return this.error && this.error.includes('suporte');
    }
  },
  methods: {
    async fetchOperadoras() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('http://localhost:5000/buscar-operadoras', {
          params: { query: this.searchQuery.toLowerCase() },
          timeout: 10000
        });
        
        if (response.data.error) {
          throw new Error(response.data.error);
        }
        
        this.operadoras = response.data.data || [];
        
      } catch (err) {
        console.error('Erro na requisição:', err);
        this.error = this.getErrorMessage(err);
        this.operadoras = [];
      } finally {
        this.loading = false;
      }
    },
    getErrorMessage(err) {
      if (err.message.includes('timeout')) {
        return 'A requisição demorou muito. Verifique sua conexão.';
      }
      if (err.response?.status === 404) {
        return 'Endpoint não encontrado. Contate o suporte.';
      }
      if (err.response?.status === 503) {
        return 'Serviço temporariamente indisponível. Tente novamente mais tarde.';
      }
      return err.message || 'Erro ao buscar dados. Tente novamente.';
    },
    handleSearch() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.fetchOperadoras();
      }, this.debounceDelay);
    },
    sortBy(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },
    formatCNPJ(cnpj) {
      if (!cnpj) return 'Não informado';
      const digits = cnpj.toString().replace(/\D/g, '');
      return digits.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    },
    formatLabel(key) {
      const labels = {
        'razao_social': 'Razão Social',
        'nome_fantasia': 'Nome Fantasia',
        'registro_ans': 'Registro ANS',
        'cnpj': 'CNPJ',
        'modalidade': 'Modalidade',
        'logradouro': 'Endereço',
        'municipio': 'Município',
        'uf': 'UF',
        'cep': 'CEP',
        'ddd': 'DDD',
        'telefone': 'Telefone',
        'fax': 'Fax',
        'endereco_eletronico': 'Email',
        'representante': 'Representante',
        'cargo_representante': 'Cargo do Representante'
      };
      return labels[key] || key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    },
    showDetails(operadora) {
      this.selectedOperadora = operadora;
      document.body.style.overflow = 'hidden';
    },
    closeModal() {
      this.selectedOperadora = null;
      document.body.style.overflow = 'auto';
    },
    clearSearch() {
      this.searchQuery = '';
      this.fetchOperadoras();
    },
    exportToCSV() {
      const headers = Object.keys(this.operadoras[0]);
      const csvContent = [
        headers.join(';'),
        ...this.operadoras.map(row => 
          headers.map(fieldName => 
            JSON.stringify(row[fieldName] || '')
          ).join(';')
        )
      ].join('\n');

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      saveAs(blob, `operadoras_${this.searchQuery || 'todos'}.csv`);
    }
  },
  mounted() {
    this.fetchOperadoras();
  }
}
</script>

<style scoped>

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f7fa;
  color: #333;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1.5rem;
  text-align: center;
}

.app-title {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.search-container {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  justify-content: center;
}

.search-input {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 6px;
  width: 100%;
  max-width: 500px;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-button {
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #2980b9;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* Estados */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  background-color: #fdecea;
  color: #d32f2f;
  padding: 1.5rem;
  border-radius: 6px;
  text-align: center;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #b71c1c;
}

.support-text {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.clear-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #7f8c8d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.clear-button:hover {
  background-color: #5d6d7e;
}

/* Tabela */
.results-container {
  margin-top: 1.5rem;
}

.results-info {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.export-button {
  padding: 0.3rem 0.8rem;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.export-button:hover {
  background-color: #219653;
}

.table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.operadoras-table {
  width: 100%;
  border-collapse: collapse;
}

.operadoras-table th {
  background-color: #3498db;
  color: white;
  padding: 1rem;
  text-align: left;
  cursor: pointer;
  user-select: none;
  position: relative;
}

.operadoras-table th:hover {
  background-color: #2980b9;
}

.operadoras-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.operadoras-table tr:last-child td {
  border-bottom: none;
}

.operadoras-table tr:hover td {
  background-color: #f5f9fc;
}

.details-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.2rem;
}

.details-button:hover {
  transform: scale(1.1);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.detail-row {
  display: flex;
  gap: 0.5rem;
}

.detail-label {
  font-weight: bold;
  min-width: 150px;
}

/* Rodapé */
.app-footer {
  text-align: center;
  padding: 1rem;
  background-color: #2c3e50;
  color: white;
  font-size: 0.9rem;
}

/* Responsivo */
@media (max-width: 768px) {
  .app-header {
    padding: 1rem;
  }
  
  .app-title {
    font-size: 1.4rem;
  }
  
  .search-container {
    flex-direction: column;
  }
  
  .search-button {
    width: 100%;
  }
  
  .app-main {
    padding: 1rem;
  }
  
  .operadoras-table th, 
  .operadoras-table td {
    padding: 0.75rem;
  }

  .modal-details {
    grid-template-columns: 1fr;
  }

  .detail-row {
    flex-direction: column;
    gap: 0.2rem;
  }

  .detail-label {
    min-width: auto;
  }
}
</style>