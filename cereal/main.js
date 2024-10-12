
import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";

const term = new Terminal({
  scrollback: 10_000,
  fontWeight: 100,
  fontSize: 20,
  fontFamily: "Ubuntu Mono",
  theme: {
    background: "#1c1c1e",
  },
});

const fitAddon = new FitAddon();
term.loadAddon(fitAddon);

document.addEventListener("DOMContentLoaded", async () => {
  const terminalElement = document.getElementById("terminal");
  if (terminalElement) {
    term.open(terminalElement);
    fitAddon.fit();

    window.addEventListener("resize", () => {
      fitAddon.fit();
    });
  }
});

term.open(document.getElementById("terminal"));
term.writeln("Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ");
