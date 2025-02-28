document.getElementById('searchForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const searchQuery = document.getElementById('searchQuery').value;
  fetch(`/search?query=${encodeURIComponent(searchQuery)}`)
    .then(response => response.json())
    .then(data => {
      const resultsList = document.getElementById('bookResults');
      resultsList.innerHTML = '';
      data.forEach(book => {
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = book.url;
        link.textContent = book.title;
        link.target = '_blank';
        const descriptionSpan = document.createElement('span');
        descriptionSpan.textContent = ` - ${book.description}`;
        listItem.appendChild(link);
        listItem.appendChild(descriptionSpan);
        resultsList.appendChild(listItem);
      });
    })
    .catch(err => {
      console.error('Error fetching data:', err);
    });
});
