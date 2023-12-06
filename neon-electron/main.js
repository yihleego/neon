const {app, BrowserWindow} = require('electron')
const path = require('node:path')

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    win.loadFile('index.html')
    return win
}

function createChildWindow() {
    const child = new BrowserWindow({
        // parent: win,
        transparent: true,
        frame: false,
        width: 1920,
        height: 1080,
        skipTaskbar: true,
        alwaysOnTop: true,

    })
    child.loadFile('child.html')
    child.maximize();
    child.setIgnoreMouseEvents(true)
    child.show()
    child.on('close', e => {
        e.preventDefault();
    });
    return child
}

app.whenReady().then(() => {
    const win = createWindow()
    const child = createChildWindow()
    app.on('activate', () => {
        const allWindows = BrowserWindow.getAllWindows()
        if (allWindows.length === 0) {
            createWindow()
        } else if (allWindows.length === 1 && allWindows[0] === child) {
            createWindow()
        }
    })
    win.webContents.openDevTools({ mode: 'detach' })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

