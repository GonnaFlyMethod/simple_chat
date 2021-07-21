function scrollToBottom(ellement)
{
    var objDiv = document.getElementById("scrollarea");
    objDiv.scrollTop = objDiv.scrollHeight;
}



async function getNumOfPages(url){
    return axios.get(url).then(function(resp) {
        var page_size;
        var total_objects;
        var pages_total;

        total_objects = resp.data.count;
        page_size = resp.data.results.length;
        pages_total = Math.ceil(total_objects / page_size);
        return pages_total;
    }).catch(function(error){
        console.log(error);
    });
};


async function getPageMessages(url)
{
    return axios.get(url).then(function(resp) {
        var data = resp.data.results;

        return data;
    }).catch(function(error){
        console.log(error);
    });
}


async function insertMessagesFromPage(target, list_of_messages, status)
{

    if (status == 'initial')
    {
        for(var i=0; i < list_of_messages.length; i++)
        {
            var msg_unit = list_of_messages[i];
            var username = msg_unit.username;
            var timestamp = msg_unit.timestamp;
            var message = msg_unit.message;

            var msg_template = `
                    <li>
                        <div id="message">
                            <b>${username}</b><br>
                            <i>${timestamp}</i><br>

                            <p>${message}</p>
                        </div>
                    </li>
                `;

            $(target).append(msg_template);
        }
    }
    else
    {
        for(var i = list_of_messages.length - 1; i >= 0; i--)
        {
            var msg_unit = list_of_messages[i];
            var username = msg_unit.username;
            var timestamp = msg_unit.timestamp;
            var message = msg_unit.message;

            var msg_template = `
                    <li>
                        <div id="message">
                            <b>${username}</b><br>
                            <i>${timestamp}</i><br>

                            <p>${message}</p>
                        </div>
                    </li>
                `;

            $(target).prepend(msg_template);
        }
    }
    
    
}