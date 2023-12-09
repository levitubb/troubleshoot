"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
electron_1.contextBridge.exposeInMainWorld("archives", {
    readSitePackagesSnapshot: () => electron_1.ipcRenderer.invoke("readSitePackagesSnapshot"),
    readStreamlitAppDirectory: () => electron_1.ipcRenderer.invoke("readStreamlitAppDirectory"),
});
