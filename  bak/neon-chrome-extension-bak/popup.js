document.addEventListener('DOMContentLoaded', function () {
   /* var selectButton = document.getElementById('selectButton');
    selectButton.addEventListener('click', function () {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: 'startSelection'});
        });
    });*/


    // 获取拖动容器和标题栏元素
    var dragContainer = document.getElementById('drag-container');
    var dragHeader = document.getElementById('drag-header');

    // 鼠标按下时的初始位置
    var offsetX, offsetY;

    // 鼠标按下事件监听器
    dragHeader.addEventListener('mousedown', function (e) {
        // 计算鼠标相对于拖动容器左上角的偏移
        offsetX = e.clientX - dragContainer.getBoundingClientRect().left;
        offsetY = e.clientY - dragContainer.getBoundingClientRect().top;

        // 添加鼠标移动和松开事件的监听器
        document.addEventListener('mousemove', dragMove);
        document.addEventListener('mouseup', dragEnd);
    });

    // 鼠标移动事件监听器
    function dragMove(e) {
        // 计算拖动容器的新位置
        var left = e.clientX - offsetX;
        var top = e.clientY - offsetY;

        // 设置拖动容器的新位置
        dragContainer.style.left = left + 'px';
        dragContainer.style.top = top + 'px';
    }

    // 鼠标松开事件监听器
    function dragEnd() {
        // 移除鼠标移动和松开事件的监听器
        document.removeEventListener('mousemove', dragMove);
        document.removeEventListener('mouseup', dragEnd);
    }

});