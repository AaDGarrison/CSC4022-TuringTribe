function updateSingleItem(id,text)
{
    try{
        const singleItemList= document.getElementById(id);
        singleItemList.innerHTML=text;
    }
    catch (error) {
        // Handle the error
        console.error(error);
    }
}
function getBalance(id)
{
    var query="?CardId="+id
    return fetch('/api/get-balance/'+query)
    .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
      })
    .then(data=>{
        updateSingleItem(id, data.Balance)
    })

}

