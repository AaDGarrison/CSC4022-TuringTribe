function updateTile(id,titleData)
{
    console.log(titleData)
    try{
        const title= document.getElementById(id+"-Title");
        title.textContent=titleData;
    }
    catch (error) {
        // Handle the error
        console.error(error);
    }


}
function getTitle(id)
{
    var query="?CardId="+id
    return fetch('/api/get-card-name/'+query)
    .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
      })
    .then(data=>{
        updateTile(id, data.CardName.toString())
    })


}