var isSelecting = false;

document.addEventListener('mousedown', function (event) {
    if (isSelecting) {
        var target = event.target;
        var xpath = getXPath(target);
        var cssSelector = getCssSelector(target);

        console.log('XPath:', xpath);
        console.log('CSS Selector:', cssSelector);
        alert(xpath)
        alert(cssSelector)
        // TODO: Send the XPath and CSS Selector to your extension's background script or perform any other action.

        isSelecting = false;
    }
});

chrome.runtime.onMessage.addEventListener(function (request, sender, sendResponse) {
    if (request.action === 'startSelection') {
        isSelecting = true;
    }
});

function getXPath(element) {
    if (element.id !== '')
        return 'id("' + element.id + '")';

    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;

    for (var i = 0; i < siblings.length; i++) {
        var sibling = siblings[i];

        if (sibling === element)
            return getXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';

        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }
}

function getCssSelector(element) {
    var path = [];
    while (element.nodeType === Node.ELEMENT_NODE) {
        var selector = element.nodeName.toLowerCase();

        if (element.id) {
            selector += '#' + element.id;
            path.unshift(selector);
            break;
        } else {
            var sibling = element;

            while (sibling && sibling.nodeType === Node.ELEMENT_NODE) {
                if (sibling.nodeName.toLowerCase() === selector) {
                    selector += ':nth-child(' + (Array.from(sibling.parentNode.children).indexOf(sibling) + 1) + ')';
                    break;
                }
                sibling = sibling.previousElementSibling;
            }
        }

        path.unshift(selector);
        element = element.parentNode;
    }

    return path.join(' > ');
}