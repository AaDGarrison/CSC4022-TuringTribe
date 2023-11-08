
function updateList(data, id) {
  if (Array.isArray(data)) {
    // Get the list element by its ID
    const list = document.getElementById(id);

    if (list) {
      // Clear existing list items
      while (list.firstChild) {
        list.removeChild(list.firstChild);
      }

      // Add list items based on 'data'
      data.forEach(item => {
        const listItem = document.createElement("li");
        listItem.textContent = item; // Use the item directly
        list.appendChild(listItem);
      });
    } else {
      console.error(`Element with ID '${id}' not found.`);
    }
  } else {
    console.error(`'data' is not a valid array.`);
  }
}
function GetTransaction(id) {
  // Fetch data from the API
  return fetch('/api/get-transactions/?StartDate=2021-03-25&StopDate=2021-12-25')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      // Parse the JSON response
      return response.json();
    })
    .then(data=>{
      var stringList=[]
      for(var item of data)
      {
        stringList.push("Source:"+item.merchant+" Amount :"+item.amount +" Date: "+item.date)

      }
      updateList(stringList,id);
      return
    })
    .catch(error => {
      // Handle any errors that occurred during the fetch
      console.log("ERROR");
      // You can choose to re-throw the error for further handling or return an empty list
      throw error; // Re-throw the error
    });
}