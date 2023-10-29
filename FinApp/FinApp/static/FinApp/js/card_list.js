
function updateList(data,id)
{
    const list = document.getElementById(id);

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


}