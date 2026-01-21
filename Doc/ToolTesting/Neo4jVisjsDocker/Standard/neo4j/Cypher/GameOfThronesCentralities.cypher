LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/johnymontana/neovis.js/master/examples/data/got-centralities.csv'
AS row
MATCH (c:Character {name: row.name})
SET c.community = toInteger(row.community), c.pagerank = toFloat(row.pagerank)
