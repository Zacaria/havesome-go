importScripts('wasm_exec.js');
let started = false;
onmessage = async ({ data }) => {
  try {
    if (!started) {
      const go = new Go();
      const response = await fetch('engine.wasm');
      if (!response.ok) throw new Error('Moteur indisponible (' + response.status + ').');
      const { instance } = await WebAssembly.instantiate(await response.arrayBuffer(), go.importObject);
      go.run(instance).catch(error => postMessage({ error: String(error) }));
      started = true;
    }
    postMessage({ output: self.runGo(data.source) });
  } catch (error) {
    postMessage({ error: String(error) });
  }
};
