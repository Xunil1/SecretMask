SELECT p.title,
       r.barcode,
       r.price
FROM pos p
JOIN reports r ON p.id = r.pos_id
GROUP BY p.title, r.barcode, r.price
ORDER BY p.title;

/*
На мой взгляд тут не нужна агрегатная функция
*/