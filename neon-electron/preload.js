window.addEventListener('DOMContentLoaded', () => {

    // Clean up resources if needed
    const replaceText = (selector, text) => {
        const element = document.getElementById(selector)
        if (element) element.innerText = text
    }

    for (const type of ['chrome', 'node', 'electron']) {
        replaceText(`${type}-version`, process.versions[type])
    }


    const ffi = require('ffi-napi')
    const ref = require('ref-napi');
    const StructType = require('ref-struct-napi')

    var winapi = {};
    winapi.void = ref.types.void;
    winapi.PVOID = ref.refType(winapi.void);
    winapi.HANDLE = winapi.PVOID;
    winapi.HWND = winapi.HANDLE;
    winapi.WCHAR = ref.types.char;
    winapi.LPCWSTR = ref.types.CString;
    winapi.UINT = ref.types.uint;

// Try to load message box function as defined in
//   https://msdn.microsoft.com/en-us/library/windows/desktop/ms645505%28v=vs.85%29.aspx
    var current = ffi.Library("user32.dll", {
        'MessageBox': ['int', [winapi.HWND, winapi.LPCWSTR, winapi.LPCWSTR, winapi.UINT]]
    });
    current.MessageBox(0, "sss", "sss", 0);


    ffi.Library("UIAutomationCore.dll", {
        "CoCreateInstance": ["int", ["string", "int", "int", "string", "pointer"]],
    })
})