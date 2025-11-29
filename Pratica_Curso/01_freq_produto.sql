WITH tb_freq_abs AS (

    SELECT descProduto,
        count(idTransacao) AS FreqAbs 
    FROM points

    GROUP BY descProduto
),

tb_freq_abs_acum AS (

    SELECT *,
        SUM(FreqAbs) OVER (ORDER BY descProduto) AS FreqCumulativa,
        1.0 * FreqAbs / (SELECT sum(FreqAbs) FROM tb_freq_abs) AS FreqRelativa
    FROM tb_freq_abs
)

SELECT *,
       sum(FreqRelativa) OVER (ORDER BY descProduto) AS FreqRelatovaAcum

FROM tb_freq_abs_acum