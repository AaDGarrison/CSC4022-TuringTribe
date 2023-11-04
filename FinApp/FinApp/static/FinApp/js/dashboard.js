
document.addEventListener("DOMContentLoaded", initCardData)

function initCardData()
{
    for(i=0; i<cardIdList.length;i++)
    {
        console.log(cardIdList[i]);
        updateList(GetTransaction(i),cardIdList[i])
    }
}