
document.addEventListener("DOMContentLoaded", initCardData)

function initCardData()
{
    for(i=0; i<cardIdList.length;i++)
    {
        console.log("/"+cardIdList[i]+"/");
        if(cardIdList[i]>=1000&&cardIdList[i]<2000){
            GetTransaction(cardIdList[i].toString());
        }
        else if(cardIdList[i]>=2000&&cardIdList[i]<3000)
        {
            getBalance(cardIdList[i].toString())
        }
        getTitle(cardIdList[i].toString())
    }
}