-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS estoque_pecas;
USE estoque_pecas;

-- ===========================
-- 1. TABELA DE GRUPOS
-- ===========================
CREATE TABLE grupos (
    id_grupo      INT PRIMARY KEY AUTO_INCREMENT,
    nome_grupo    VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- ===========================
-- 2. TABELA DE FORNECEDORES
-- ===========================
CREATE TABLE fornecedores (
    id_fornecedor     INT PRIMARY KEY AUTO_INCREMENT,
    nome_fornecedor   VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- ===========================
-- 3. TABELA DE PECAS
-- ===========================
CREATE TABLE pecas (
    id_peca       INT PRIMARY KEY AUTO_INCREMENT,
    id_grupo      INT NOT NULL,
    codigo        VARCHAR(50) NOT NULL,
    descricao     VARCHAR(200) NOT NULL,
    local         VARCHAR(20),
    estoque_atual INT DEFAULT 0,

    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo)
) ENGINE=InnoDB;

-- ===========================
-- 4. TABELA DE MOVIMENTAÇÕES
-- ===========================
CREATE TABLE movimentacoes (
    id_mov            INT PRIMARY KEY AUTO_INCREMENT,
    id_peca           INT NOT NULL,
    quantidade        INT NOT NULL,
    tipo_mov          VARCHAR(20) NOT NULL, -- Entrada ou Saída
    id_fornecedor     INT,
    data_movimentacao DATE NOT NULL,

    FOREIGN KEY (id_peca) REFERENCES pecas(id_peca),
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
) ENGINE=InnoDB;

-- ===========================================
-- 5. INSERT DE GRUPOS
-- ===========================================
INSERT INTO grupos (nome_grupo) VALUES
('Grupo 75'),
('Grupo 80');

-- ===========================================
-- 6. INSERT DE FORNECEDORES
-- ===========================================
INSERT INTO fornecedores (nome_fornecedor) VALUES
('FerroMais'),
('MetalTec'),
('HidroMax'),
('AquaParts');

-- ===========================================
-- 7. INSERT DE PEÇAS
-- ===========================================
INSERT INTO pecas (id_grupo, codigo, descricao, local) VALUES
(1, '8841', 'Cabo 182', 'C-1'),
(1, '123', 'Corpo 1745', 'B-3'),
(2, '5655', 'Canopla do chuveiro', 'A-45'),
(1, '6846', 'Corpo de monoc', 'J-42'),
(1, '646846', 'Porca c42', 'F-51'),
(2, '7891', 'Volante de monoc', 'G-20'),
(2, '46513', 'Tubo 1897', 'E80');

-- ===========================================
-- 8. MOVIMENTAÇÕES
-- ===========================================
INSERT INTO movimentacoes (id_peca, quantidade, tipo_mov, id_fornecedor, data_movimentacao) VALUES
(3, 250, 'Entrada', 3, '2024-11-10'),
(5, 250, 'Entrada', 3, '2024-11-14'),
(6, 1050, 'Saída', 2, '2024-11-17'),
(2, 150, 'Saída', 2, '2024-11-18'),
(1, 100, 'Entrada', 1, '2024-11-20'),
(4, 500, 'Saída', 1, '2024-11-21'),
(7, 410, 'Saída', 4, '2024-11-22');

-- ===========================================
-- 9. TRIGGER PARA ATUALIZAÇÃO DO ESTOQUE
-- ===========================================
DELIMITER //
CREATE TRIGGER atualizar_estoque
AFTER INSERT ON movimentacoes
FOR EACH ROW
BEGIN
    UPDATE pecas
    SET estoque_atual = estoque_atual +
        (CASE WHEN NEW.tipo_mov = 'Entrada' THEN NEW.quantidade ELSE -NEW.quantidade END)
    WHERE id_peca = NEW.id_peca;
END //
DELIMITER ;

-- ================================
-- FIM DO SCRIPT
-- ================================
