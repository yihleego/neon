document.addEventListener('DOMContentLoaded', function () {
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        var activeTab = tabs[0];
        chrome.debugger.attach({tabId: activeTab.id}, "1.2", function () {
            console.log("Attached to tab");
            // 在这里发送消息给Python调试器
            fetch('http://localhost:18000/ping');
        });
    });

// 在chrome.debugger.attach的回调中
    /*chrome.debugger.sendCommand({tabId: activeTab.id}, "Debugger.enable", {}, function () {
        console.log("Debugger enabled");
        // 发送其他命令给Python调试器
    });*/
});
