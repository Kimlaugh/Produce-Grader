// main.js
const { app, BrowserWindow,Menu } = require('electron');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    fullscreen: false, // Run in full-screen mode
    webPreferences: {
      nodeIntegration: true,
    }
  });

  // Load the Flask app (assuming it runs on port 5000)
  mainWindow.loadURL('http://127.0.0.1:5000/');

  mainWindow.on('closed', () => {
    app.quit();
  
    
  });

  let menu = Menu.buildFromTemplate([
    {
        label: 'Menu Options',
        submenu: [
            {
                label: 'Quit',
                click: () => {
                    app.quit(); // Quit the application when clicked
                }
            },
            {
                label: 'Reload',
                click: () => {
                    mainWindow.reload(); // Reload the main window when clicked
                }
            }
        ]
    }
]);

  Menu.setApplicationMenu(menu);
 
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
