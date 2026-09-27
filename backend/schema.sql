-- Schema do banco de dados de progresso do "Prática Python para Dados"
-- Rode manualmente com: sqlite3 progresso.db < schema.sql
-- (o app.py também cria essas tabelas sozinho na primeira vez que roda)

CREATE TABLE IF NOT EXISTS progresso (
    exercicio_id   TEXT PRIMARY KEY,
    concluido      INTEGER NOT NULL DEFAULT 0,   -- 0 = false, 1 = true
    codigo         TEXT,                          -- último código salvo pelo usuário nesse exercício
    atualizado_em  TEXT NOT NULL                  -- ISO 8601 (ex: 2026-09-27T10:00:00)
);

CREATE TABLE IF NOT EXISTS tentativas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    exercicio_id  TEXT NOT NULL,
    sucesso       INTEGER NOT NULL,   -- 0 = errou, 1 = acertou
    mensagem      TEXT,               -- feedback que o app mostrou nessa tentativa
    criado_em     TEXT NOT NULL       -- ISO 8601
);

-- Exemplos de consultas que você pode rodar para praticar SQL no seu próprio histórico real:

-- Quantas tentativas totais e quantos acertos por exercício:
-- SELECT exercicio_id,
--        COUNT(*) AS tentativas,
--        SUM(sucesso) AS acertos
-- FROM tentativas
-- GROUP BY exercicio_id
-- ORDER BY tentativas DESC;

-- Exercícios em que você mais errou antes de acertar:
-- SELECT exercicio_id, COUNT(*) AS erros
-- FROM tentativas
-- WHERE sucesso = 0
-- GROUP BY exercicio_id
-- ORDER BY erros DESC;
