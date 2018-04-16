const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')
const Menu = electron.Menu

/*************************************************************
 * py process
 *************************************************************/

const PY_DIST_FOLDER = 'pycalcdist'
const PY_FOLDER = 'pycalc'
const PY_MODULE = 'api' // without .py suffix

let pyProc = null
let pyPort = null

const guessPackaged = () => {
    const fullPath = path.join(__dirname, PY_DIST_FOLDER)
    return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
    if (!guessPackaged()) {
        return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
    }
    if (process.platform === 'win32') {
        return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
    }
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const selectPort = () => {
    pyPort = 4242
    return pyPort
}

const createPyProc = () => {
    let script = getScriptPath()
    let port = '' + selectPort()

    if (guessPackaged()) {
        pyProc = require('child_process').execFile(script, [port])
    } else {
        pyProc = require('child_process').spawn('python', [script, port])
    }

    if (pyProc != null) {
        //console.log(pyProc)
        console.log('child process success on port ' + port)
    }
}

const exitPyProc = () => {
    pyProc.kill()
    pyProc = null
    pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)


/*************************************************************
 * window management
 *************************************************************/

let mainWindow = null

const createWindow = () => {
    mainWindow = new BrowserWindow({ width: 1600, height: 800 })
    mainWindow.loadURL(require('url').format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
    }))
    const mainMenu = Menu.buildFromTemplate(mainMenuTemplate);
    Menu.setApplicationMenu(mainMenu);
    mainWindow.on('closed', () => {
        mainWindow = null
    })
    //mainWindow.webContents.openDevTools()
}

const mainMenuTemplate = [
    // Each object is a dropdown
    {
        label: 'File',
        submenu: [{
            label: 'Quit',
            accelerator: process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
            click() {
                app.quit();
            }
        }]
    }
];

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow()
    }
})