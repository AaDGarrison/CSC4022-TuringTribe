
function updateList(data,id)
{
   list = document.getElementById(id);

   if (list && Array.isArray(data)) {
    // Clear list items
    while (list.firstChild) {
      list.removeChild(list.firstChild);
    }

    // Update list
    data.forEach(item => {
      const listItem = document.createElement("li");
      listItem.textContent = item.name;
      list.appendChild(listItem);
    });
  } else {
    console.error(`Element with ID '${id}' not found, or 'data' is not a valid array.`);
  }


}
function GetTransaction(id)
{
  fetch('http://192.168.1.11:9000/api/get-transactions/?StartDate=2021-03-25&StopDate=2021-12-25')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the response body as JSON
  })
  .then(data => {
    // Work with the JSON data
    console.log(data);
  })
  .catch(error => {
    // Handle any errors that occurred during the fetch
    console.error('Fetch error:', error);
  });


}