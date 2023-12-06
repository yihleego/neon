from pychrome import Browser

# 连接到远程Chrome浏览器
chrome = Browser()
tab = chrome.new_tab(url="http://localhost:9222/")

# 打开一个网页
tab.Page.navigate(url="https://www.example.com")

# 等待加载完成
tab.wait(5)

# 获取网页的标题
result = tab.Runtime.evaluate(expression="document.title")
print("Page Title:", result['result']['value'])

# 关闭连接
chrome.close_tab(tab)