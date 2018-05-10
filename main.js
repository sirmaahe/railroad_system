const {app, BrowserWindow} = require('electron')

function createWindow() {
    let win = new BrowserWindow({width: 1024, height: 768})
    win.on('closed', () => {
        win = null
    })

// Load a remote URL
    win.loadURL('http://localhost:5000')
}

app.on('ready', createWindow)