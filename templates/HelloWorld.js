const fs = require('fs');
const os = require('os');
const path = require('path');

// デスクトップパス取得
const desktopPath = path.join(os.homedir(), 'Desktop');
const filePath = path.join(desktopPath, `hello_js_${Date.now()}.txt`);

// "Hello, world!" を書き込み
fs.writeFileSync(filePath, "Hello, world!", "utf-8");

console.log(`File created: ${filePath}`);
