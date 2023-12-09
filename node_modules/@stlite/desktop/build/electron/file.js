"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.walkRead = void 0;
const fsPromises = require("fs/promises");
const path = require("path");
/**
 * Returns an object whose keys are absolute paths of the files and values are the file contents.
 * Note that the paths are OS-specific, "/" for POSIX and "\" for Windows,
 * so this function is only expected to be called from `walkRead()` that converts the paths to be POSIX.
 */
async function walkReadAbsPath(dirPath) {
    const fileContents = {};
    const childNames = await fsPromises.readdir(dirPath);
    await Promise.all(childNames.map(async (childName) => {
        const childPath = path.join(dirPath, childName);
        const stat = await fsPromises.stat(childPath);
        if (stat.isDirectory()) {
            const childFileContents = await walkReadAbsPath(childPath);
            Object.assign(fileContents, childFileContents);
        }
        else {
            const fileBin = await fsPromises.readFile(childPath);
            fileContents[childPath] = fileBin;
        }
    }));
    return fileContents;
}
async function walkRead(dirPath) {
    const fileContents = await walkReadAbsPath(dirPath);
    const relPathFileContents = {};
    Object.keys(fileContents).forEach((absPath) => {
        const relPath = path.relative(dirPath, absPath);
        const posixRelPath = relPath.split(path.sep).join(path.posix.sep); // Convert the path separators on Windows to POSIX ones.
        relPathFileContents[posixRelPath] = fileContents[absPath];
    });
    return relPathFileContents;
}
exports.walkRead = walkRead;
