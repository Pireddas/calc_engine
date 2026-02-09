# Financial Metrics API (v0.1.0)

## 📌 Visão Geral

A **Financial Metrics API** é uma solução de análise quantitativa avançada voltada para a gestão de ativos e risco financeiro. Diferente de scripts financeiros simples, este projeto foi construído sob princípios de **Domain-Driven Design (DDD)** e **Arquitetura Limpa**, focando em três pilares:

1.  **Precisão Quantitativa:** Métricas de performance, risco de cauda (Tail Risk) e análise de portfólio.
2.  **Governança:** Controle de acesso rígido via API Keys com persistência segura em banco de dados.
3.  **Observabilidade:** Rastreabilidade total de requisições, logs estruturados e monitoramento de performance.

---

## 🏗️ Arquitetura e Design

O projeto utiliza uma divisão por **Domínios**, isolando a lógica de negócio das implementações técnicas e provedores externos.

### Estrutura de Camadas
* **Domains (`app/domains`):** O coração da aplicação. Cada domínio (Finance, Risk, Portfolio, Auth) possui seus próprios serviços, esquemas (Pydantic) e definições de interface.
* **Infrastructure (`app/infrastructure`):** Implementações concretas de acesso a dados (integração com Yahoo Finance via `yfinance`) e persistência (SQLite para gestão de chaves).
* **Application (`app/application`):** Configurações globais via Pydantic Settings, bootstrapping do banco de dados e o container de dependências.
* **Platform (`app/platform`):** Recursos transversais (cross-cutting concerns) como middlewares de segurança, auditoria e utilitários de gestão.

---

## 🧩 Domínios do Sistema

### 🔐 Auth & Governance
Responsável pelo ciclo de vida de credenciais e segurança da API.
* **Segurança:** Middleware `SQLiteAuthMiddleware` que intercepta requisições e valida headers `X-API-KEY` usando hash SHA-256.
* **Gestão:** Scripts e serviços para criação, ativação e revogação de chaves com associação a proprietários (*owners*).

### 📊 Finance Metrics
Análise de performance e volatilidade de ativos individuais.
* **Métricas:** Retorno Total, CAGR (Taxa de Crescimento Anual Composta), Volatilidade Anualizada e Sharpe Ratio.
* **Validação:** Engine de validação de tickers para garantir a integridade dos dados históricos processados.

### ⚠️ Risk Analysis
Foco em estatísticas de eventos extremos e gestão de perdas.
* **Tail Risk:** Cálculo de **VaR (Value at Risk)** e **CVaR (Conditional VaR)** via simulação histórica.
* **Estresse:** Suporte a múltiplos níveis de confiança (95%, 98%, 99% e 99.9%).

### 📈 Portfolio Analysis
Análise de cestas de ativos e diversificação.
* **Correlação:** Geração de matriz de correlação para identificar dependências entre ativos.
* **Métricas Agregadas:** Volatilidade do portfólio e performance ponderada.

---

## 🛠️ Tecnologias e Boas Práticas
* **FastAPI:** Framework moderno de alta performance com suporte a tipagem estática.
* **Pydantic:** Validação de dados e contratos de API (Schemas).
* **Pandas & NumPy:** Engine matemática para processamento de séries temporais financeiras.
* **Poetry:** Gestão de dependências e isolamento de ambiente.
* **Observabilidade:** Middleware de logs estruturados com `request_id` e métricas de tempo de execução.

---

## 🚀 Evolução da Arquitetura (Roadmap)

O projeto foi desenhado para ser extensível, com um roadmap claro para ambientes de produção em larga escala:

1.  **Injeção de Dependências Nativa:** Migrar a instanciação manual para o sistema de `Depends` do FastAPI ou um container IoC dedicado.
2.  **Concurrency (Async/Await):** Tornar as chamadas à infraestrutura (APIs de mercado) assíncronas para aumentar o throughput.
3.  **Caching Layer:** Implementar cache distribuído (Redis) para dados de mercado, minimizando latência e custos de API.
4.  **Database Migration:** Substituir a gestão manual do banco por **Alembic** para versionamento de esquema.
5.  **Persistência Configurável:** (SQLite / PostgreSQL)
    - Necessidade de suportar ambientes distintos (dev vs produção)
    - SQLite é suficiente para desenvolvimento local e testes
    - PostgreSQL é mais adequado para concorrência, volume e produção


---

## ▶️ Executando o Projeto

1.  **Instalação:**
    ```bash
    poetry install
    ```
2.  **Configuração:**
    Configure o arquivo `.env` com as definições de `RISK_FREE_RATE`, `DEFAULT_BENCHMARK` e `DB_PATH`.
3.  **Execução:**
    ```bash
    $env:OPENAI_API_KEY="your_api_key_here"
    poetry run python main.py
    
    # http://127.0.0.1:8000/
    ```
4.  Criar uma **API Key** utilizando a ferramenta: `app/platform/utils/manage_keys.py`
    ```bash
    python -m app.platform.utils.manage_keys
    ```

6.  **Documentação:**
    Acesse `/docs` para visualizar o Swagger UI ou `/redoc` para documentação técnica.

---
📌 *Designed for governance. Built for evolution.*

