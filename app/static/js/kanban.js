
// taken from : https://plainjs.com/javascript/ajax/send-ajax-get-and-post-requests-47/
function postAjax(url, data, success) {
    var params = typeof data == 'string' ? data : Object.keys(data).map(
            function(k){ return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
        ).join('&');

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    xhr.open('POST', url);
    xhr.onreadystatechange = function() {
        if (xhr.readyState>3 && xhr.status==200) { success(xhr.responseText); }
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(params);
    return xhr;
}

// taken from: cant remember, really appreciate it though, 
//             if you know let me know so i can credit them.
var cards = document.querySelectorAll('.card');
for (var i = 0, n = cards.length; i < n; i++) {
    var card = cards[i];
    card.draggable = true;
};
var board = document.getElementById('board');
var hideMe;
board.onselectstart = function(e) {
    e.preventDefault();
}
board.ondragstart = function(e) {
    console.log('dragstart');
    hideMe = e.target;
    e.dataTransfer.setData('card', e.target.id);
    e.dataTransfer.effectAllowed = 'move';
};
board.ondragend = function(e) {
    e.target.style.visibility = 'visible';
};
var lastEneterd;
board.ondragenter = function(e) {
    console.log('dragenter');
    if (hideMe) {
        hideMe.style.visibility = 'hidden';
        hideMe = null;
    }
    // Save this to check in dragleave.
    lastEntered = e.target;
    var section = closestWithClass(e.target, 'section');
    // TODO: Check that it's not the original section.
    if (section) {
        section.classList.add('droppable');
        e.preventDefault(); // Not sure if these needs to be here. Maybe for IE?
        return false;
    }
};

board.ondragover = function(e) {
    // TODO: Check data type.
    // TODO: Check that it's not the original section.
    if (closestWithClass(e.target, 'section')) {
        e.preventDefault();
    }
};

board.ondragleave = function(e) {
    // FF is raising this event on text nodes so only check elements.
    if (e.target.nodeType === 1) {
        // dragleave for outer elements can trigger after dragenter for inner elements
        // so make sure we're really leaving by checking what we just entered.
        // relatedTarget is missing in WebKit: https://bugs.webkit.org/show_bug.cgi?id=66547
        var section = closestWithClass(e.target, 'section');
        if (section && !section.contains(lastEntered)) {
            section.classList.remove('droppable');
        }
    }
    lastEntered = null; // No need to keep this around.
};

board.ondrop = function(e) {
    var section = closestWithClass(e.target, 'section');
    var id = e.dataTransfer.getData('card');
    if (id) {
        var card = document.getElementById(id);
        // Might be a card from another window.
        if (card) {
            if (section !== card.parentNode) {
                section.appendChild(card);
                var response = postAjax('/update_status', 
                                        {'taskid': card.id, 'statusname': section.id}, 
                                        function(data){ console.log(data); })
                setTimeout(function() {
                    window.location.reload(true);
                }, 100);
            }
        } else {
            alert('couldn\'t find card #' + id);
        }
    }
    section.classList.remove('droppable');
    e.preventDefault();
};

function closestWithClass(target, className) {
    while (target) {
        if (target.nodeType === 1 &&
            target.classList.contains(className)) {
            return target;
        }
        target = target.parentNode;
    }
    return null;
}
