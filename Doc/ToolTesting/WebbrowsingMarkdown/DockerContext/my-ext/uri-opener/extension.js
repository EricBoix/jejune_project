const vscode = require('vscode');

function activate(context) {
    vscode.window.showInformationMessage('URI Range Opener activated!');

    // Create hidden webview to read URL hash
    const panel = vscode.window.createWebviewPanel(
        'uriReader',
        'URI Reader',
        { viewColumn: vscode.ViewColumn.Active, preserveFocus: true },
        { enableScripts: true }
    );

    panel.webview.html = `<!DOCTYPE html>
    <html>
    <body>
    <script>
        const vscode = acquireVsCodeApi();

        function parseHash(hash) {
            if (!hash || !hash.startsWith('#sel=')) return null;
            const content = hash.slice(5);
            const solo = content.includes('&solo');
            const sel = decodeURIComponent(content.replace('&solo', ''));
            return { sel, solo };
        }

        function checkHash() {
            const parsed = parseHash(window.location.hash);
            if (parsed) {
                vscode.postMessage({ type: 'selection', data: parsed.sel, solo: parsed.solo });
            }
        }

        // Check immediately and on hash change
        checkHash();
        window.addEventListener('hashchange', checkHash);

        // Also check parent/top window
        try {
            const parsed = parseHash(window.top.location.hash);
            if (parsed) {
                vscode.postMessage({ type: 'selection', data: parsed.sel, solo: parsed.solo });
            }
        } catch(e) {}

        // Close after checking
        setTimeout(() => vscode.postMessage({ type: 'done' }), 500);
    </script>
    </body>
    </html>`;

    panel.webview.onDidReceiveMessage(async (msg) => {
        if (msg.type === 'selection' && msg.data) {
            // Parse: /path/file.md:sl:sc:el:ec
            const match = msg.data.match(/^(.+):(\d+):(\d+):(\d+):(\d+)$/);
            if (match) {
                const [, file, sl, sc, el, ec] = match;
                panel.dispose();
                if (msg.solo) {
                    await vscode.commands.executeCommand('workbench.action.closeAllEditors');
                }
                await openFileWithRange(file, parseInt(sl), parseInt(sc), parseInt(el), parseInt(ec));
                return;
            }
        }
        if (msg.type === 'done') {
            panel.dispose();
        }
    });

    // Command for manual trigger
    const command = vscode.commands.registerCommand('uri-opener.openRange', async (args) => {
        if (!args || !args.file) {
            vscode.window.showErrorMessage('uri-opener.openRange: missing file argument');
            return;
        }
        await openFileWithRange(args.file, args.sl, args.sc, args.el, args.ec);
    });

    // UriHandler for vscode:// URIs
    const uriHandler = vscode.window.registerUriHandler({
        handleUri(uri) {
            const params = new URLSearchParams(uri.query);
            const file = params.get('file');
            if (file) {
                openFileWithRange(
                    file,
                    parseInt(params.get('sl')) || 1,
                    parseInt(params.get('sc')) || 1,
                    parseInt(params.get('el')) || 1,
                    parseInt(params.get('ec')) || 1
                );
            }
        }
    });

    context.subscriptions.push(command, uriHandler);
}

async function openFileWithRange(file, sl = 1, sc = 1, el = sl, ec = sc) {
    const startLine = Math.max(0, sl - 1);
    const startChar = Math.max(0, sc - 1);
    const endLine = Math.max(0, el - 1);
    const endChar = Math.max(0, ec - 1);

    const selection = new vscode.Selection(
        new vscode.Position(startLine, startChar),
        new vscode.Position(endLine, endChar)
    );

    try {
        const uri = vscode.Uri.file(file);
        const doc = await vscode.workspace.openTextDocument(uri);
        await vscode.window.showTextDocument(doc, { selection, preview: false });
    } catch (err) {
        vscode.window.showErrorMessage(`uri-opener: ${err.message}`);
    }
}

function deactivate() {}

module.exports = { activate, deactivate };
