WITH  tb_usuario AS (

    SELECT idUsuario,
           sum(qtdPontos) AS qtdPontos
    FROM points
    GROUP BY idUsuario
),

tb_subset_mediana AS (

    SELECT qtdPontos
    FROM tb_usuario
    ORDER BY qtdPontos
    LIMIT 1 + (SELECT count(*) % 2 == 0 FROM tb_usuario)
    OFFSET (SELECT count(*) / 2 FROM tb_usuario )
),

tb_mediana AS (

    SELECT AVG(qtdPontos) AS Mediana
    FROM tb_subset_mediana
),

tb_subset_quartil_01 AS (

    SELECT qtdPontos
    FROM tb_usuario
    ORDER BY qtdPontos
    LIMIT 1 + (SELECT count(*) % 2 == 0 FROM tb_usuario)
    OFFSET (SELECT 1 * count(*) / 4 FROM tb_usuario )
),

tb_quartil_01 AS (

    SELECT AVG(qtdPontos) AS Quartil_01
    FROM tb_subset_quartil_01
),

tb_subset_quartil_03 AS (

    SELECT qtdPontos
    FROM tb_usuario
    ORDER BY qtdPontos
    LIMIT 1 + (SELECT count(*) % 2 == 0 FROM tb_usuario)
    OFFSET (SELECT 3 * count(*) / 4 FROM tb_usuario )
),

tb_quartil_03 AS (

    SELECT AVG(qtdPontos) AS Quartil_03
    FROM tb_subset_quartil_03
),

tb_status AS (

    SELECT min(qtdPontos) AS Min,
        AVG(qtdPontos) AS Media,
        max(qtdPontos) AS Max 
    FROM tb_usuario
)

SELECT *
FROM tb_status, tb_mediana, tb_quartil_01, tb_quartil_03