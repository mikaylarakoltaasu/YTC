const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
app.use(express.static('public'));
const books = JSON.parse(fs.readFileSync(path.join(__dirname, 'books.json')));
app.get('/search', (req, res) => {
  let query = req.query.query;
  if (query === undefined || query === null) {
    query = '';
  }
  query = query.toLowerCase();
  const results = [];
  for (let i = 0; i < books.length; i++) {
    if (books[i].description.toLowerCase().includes(query)) {
      results.push(books[i]);
    }
  }
  res.json(results);
});
let PORT = 3000;
if (process.env.PORT !== undefined && process.env.PORT !== null) {
  PORT = process.env.PORT;
}
app.listen(PORT, function () {
  console.log('Server is running on port ' + PORT);
});
