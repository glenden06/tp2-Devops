db = db.getSiblingDB('blog_db');
db.createCollection('posts', {
  validator: { $jsonSchema: {
    bsonType: 'object',
    required: ['titre', 'auteur', 'vues'],
    properties: {
      titre:  { bsonType: 'string' },
      auteur: { bsonType: 'string' },
      vues:   { bsonType: 'int' }
    }
  }}
});
db.posts.insertMany([
  { titre: 'Premier article',   auteur: 'Alice',   vues: 100 },
  { titre: 'Deuxieme article',  auteur: 'Bob',     vues: 200 },
  { titre: 'Troisieme article', auteur: 'Charlie', vues: 150 },
  { titre: 'Quatrieme article', auteur: 'Diana',   vues: 300 },
  { titre: 'Cinquieme article', auteur: 'Eve',     vues: 250 },
]);