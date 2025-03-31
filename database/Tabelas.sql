CREATE TABLE operadoras (
    registro_ans VARCHAR(6) PRIMARY KEY,
    cnpj VARCHAR(14),
    razao_social VARCHAR(140),
    nome_fantasia VARCHAR(140),
    modalidade VARCHAR(140),
    logradouro VARCHAR(40),
    numero VARCHAR(20),
    complemento VARCHAR(40),
    bairro VARCHAR(30),
    cidade VARCHAR(30),
    uf VARCHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(2),
    telefone VARCHAR(10),
    fax VARCHAR(10),
    endereco_eletronico VARCHAR(40),
    representante VARCHAR(50),
    cargo_representante VARCHAR(40),
    regiao_de_comercializacao INTEGER,
    data_registro_ans DATE
);

CREATE TABLE demonstracao (
    data DATE,
    registro_ans VARCHAR(6),  
    cd_conta_contabil BIGINT,
    descricao VARCHAR(140),
    vl_saldo_inicial DECIMAL(18, 2),
    vl_saldo_final DECIMAL(18, 2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)  
);




-- Quais as 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU
-- AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?
-- Query para último trimestre
SELECT 
    o.razao_social,
    o.registro_ans,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas
FROM demonstracao d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE UPPER(d.descricao) LIKE '%EVENTOS%SINISTROS%CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
  AND d.data BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE()
GROUP BY o.razao_social, o.registro_ans
ORDER BY total_despesas DESC
LIMIT 10;


-- Query para último ano
SELECT 
    o.razao_social,
    o.registro_ans,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas
FROM demonstracao d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE UPPER(d.descricao) LIKE '%EVENTOS%SINISTROS%CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
  AND d.data BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
GROUP BY o.razao_social, o.registro_ans
ORDER BY total_despesas DESC
LIMIT 10;
