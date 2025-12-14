import os

# 定義專案名稱
PROJECT_NAME = "web-rig-studio"

# 定義所有檔案的內容
files = {
    # 1. HTML 入口
    f"{PROJECT_NAME}/index.html": r"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>3D Model Viewer - Web Rig Studio</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/css/style.css">

  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }
    }
  </script>
</head>
<body>
  <div class="app">
    <div class="panel">
      <div class="panel-inner">
        <div class="header">
          <h1>WEB RIG STUDIO</h1>
          <div class="subtitle">
            專業 3D 模型查看器 - 支援 GLB/GLTF 格式，完整動畫控制與自動綁骨整合
          </div>
        </div>

        <div class="section">
          <div class="section-title"><span>模型載入</span></div>
          <div class="control">
            <label>選擇 3D 模型檔案</label>
            <label for="file" class="file-upload-btn" id="fileLabel">📁 點擊選擇 .glb 或 .gltf 檔案</label>
            <input id="file" type="file" accept=".glb,.gltf" />
            <div class="hint">建議使用 .glb 格式</div>
          </div>
          <div class="control">
            <button id="btnReset" class="secondary" disabled>🎯 重置視角</button>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section">
          <div class="section-title"><span>動畫控制</span></div>
          <div class="control">
            <label>選擇動畫片段</label>
            <select id="clipSelect" disabled><option>等待載入模型...</option></select>
          </div>
          <div class="control">
            <label>播放速度 <span class="badge" id="speedVal">1.00x</span></label>
            <div class="range-container">
              <input id="speed" type="range" min="0.1" max="2.0" step="0.05" value="1.0" disabled />
            </div>
          </div>
          <div class="control-group">
            <button id="btnPlay" disabled>▶️ 播放</button>
            <button id="btnStop" class="secondary" disabled>⏹️ 停止</button>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section">
          <div class="section-title"><span>模型資訊</span></div>
          <div class="info-grid">
            <div class="info-item"><div class="info-label">檔案名稱</div><div class="info-value" id="infoName">-</div></div>
            <div class="info-item"><div class="info-label">動畫數量</div><div class="info-value" id="infoAnims">-</div></div>
            <div class="info-item"><div class="info-label">骨架綁定</div><div class="info-value" id="infoSkinned">-</div></div>
            <div class="info-item"><div class="info-label">網格數量</div><div class="info-value" id="infoMeshes">-</div></div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section">
          <div class="section-title"><span>自動綁骨 (Backend API)</span></div>
          <div class="control">
            <label>API 伺服器網址 (ngrok)</label>
            <input type="text" id="apiUrl" placeholder="https://xxxx.ngrok-free.app" class="api-input">
            <button id="btnUpload" disabled>🚀 上傳並自動綁骨</button>
            <div class="hint">請輸入 Google Colab 產生的 Ngrok 網址</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="control">
          <div class="status" id="status">等待載入 3D 模型</div>
        </div>
      </div>
    </div>

    <div class="viewer">
      <canvas id="c"></canvas>
      <div class="spinner" id="spinner"></div>
      <div class="overlay">
        <div class="chip"><span class="chip-icon"></span><span id="chipInfo">未載入模型</span></div>
        <div class="chip"><span class="chip-icon"></span><span id="chipAnim">動畫: 無</span></div>
        <div class="chip"><span class="chip-icon"></span><span id="chipSkinned">骨架: 無</span></div>
      </div>
    </div>
  </div>
  <script type="module" src="assets/js/main.js"></script>
</body>
</html>""",

    # 2. CSS 樣式
    f"{PROJECT_NAME}/assets/css/style.css": r"""* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --primary: #00d4ff; --primary-dark: #0099cc; --secondary: #7c3aed; --bg-dark: #0a0e27; --bg-panel: rgba(15, 23, 42, 0.85); --text-primary: #ffffff; --text-secondary: #94a3b8; --border: rgba(255, 255, 255, 0.1); --success: #10b981; --warning: #f59e0b; --error: #ef4444; }
html, body { height: 100%; font-family: 'IBM Plex Sans', sans-serif; background: var(--bg-dark); color: var(--text-primary); overflow: hidden; }
body::before { content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 20% 30%, rgba(0, 212, 255, 0.15) 0%, transparent 50%), radial-gradient(ellipse at 80% 70%, rgba(124, 58, 237, 0.15) 0%, transparent 50%), linear-gradient(135deg, #0a0e27 0%, #1e1b4b 100%); z-index: -1; animation: bgShift 20s ease-in-out infinite; }
@keyframes bgShift { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
.app { display: grid; grid-template-columns: 420px 1fr; height: 100vh; gap: 0; }
.panel { background: var(--bg-panel); backdrop-filter: blur(20px); border-right: 1px solid var(--border); overflow-y: auto; overflow-x: hidden; position: relative; animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes slideInLeft { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
.panel-inner { padding: 32px 28px; }
.header { margin-bottom: 28px; padding-bottom: 24px; border-bottom: 1px solid var(--border); animation: fadeIn 0.8s ease-out 0.2s both; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
h1 { font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 8px; letter-spacing: -0.5px; }
.subtitle { font-size: 13px; color: var(--text-secondary); line-height: 1.6; font-weight: 300; }
.section { margin-bottom: 28px; animation: fadeIn 0.8s ease-out both; }
.section:nth-child(2) { animation-delay: 0.3s; } .section:nth-child(3) { animation-delay: 0.4s; } .section:nth-child(4) { animation-delay: 0.5s; }
.section-title { font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: var(--primary); margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.section-title::before { content: ''; width: 3px; height: 12px; background: linear-gradient(180deg, var(--primary), var(--secondary)); border-radius: 2px; }
.control { margin-bottom: 18px; }
label { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 8px; }
input[type="file"] { display: none; }
.file-upload-btn { width: 100%; padding: 14px 18px; background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); border: 2px dashed var(--border); border-radius: 12px; color: var(--text-primary); font-weight: 500; font-size: 14px; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; }
.file-upload-btn:hover { border-color: var(--primary); background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0, 212, 255, 0.3); }
button { width: 100%; padding: 12px 18px; background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%); border: none; border-radius: 10px; color: white; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); font-family: 'IBM Plex Sans', sans-serif; }
button:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4); }
button:disabled { opacity: 0.4; cursor: not-allowed; transform: none; box-shadow: none; }
button.secondary { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }
select, .api-input { width: 100%; padding: 12px 16px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid var(--border); border-radius: 10px; color: var(--text-primary); font-size: 14px; font-weight: 500; transition: all 0.3s; font-family: 'IBM Plex Sans', sans-serif; outline: none; }
select:hover, .api-input:focus { border-color: var(--primary); background: rgba(255, 255, 255, 0.08); }
.range-container { position: relative; }
input[type="range"] { width: 100%; height: 6px; border-radius: 3px; background: rgba(255, 255, 255, 0.1); outline: none; -webkit-appearance: none; cursor: pointer; }
input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--secondary)); cursor: pointer; box-shadow: 0 2px 8px rgba(0, 212, 255, 0.5); transition: all 0.3s; }
.badge { display: inline-block; padding: 4px 12px; background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(124, 58, 237, 0.2)); border: 1px solid var(--border); border-radius: 20px; font-size: 12px; font-weight: 600; font-family: 'Orbitron', sans-serif; color: var(--primary); }
.status { padding: 14px 16px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid var(--border); border-radius: 10px; font-size: 13px; font-weight: 500; color: var(--text-secondary); display: flex; align-items: center; gap: 10px; }
.status::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: var(--text-secondary); animation: pulse 2s ease-in-out infinite; }
.status.success::before { background: var(--success); } .status.error::before { background: var(--error); } .status.loading::before { background: var(--warning); }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.hint { font-size: 12px; color: var(--text-secondary); margin-top: 8px; line-height: 1.5; font-weight: 300; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 24px 0; }
.viewer { position: relative; background: radial-gradient(ellipse at center, rgba(30, 27, 75, 0.3) 0%, transparent 70%); }
#c { display: block; width: 100%; height: 100%; }
.overlay { position: absolute; left: 24px; top: 24px; display: flex; flex-direction: column; gap: 12px; pointer-events: none; animation: fadeIn 1s ease-out 0.6s both; }
.chip { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(20px); border: 1px solid var(--border); border-radius: 12px; padding: 10px 16px; font-size: 12px; font-weight: 500; color: var(--text-primary); display: flex; align-items: center; gap: 8px; font-family: 'IBM Plex Sans', sans-serif; }
.chip-icon { width: 6px; height: 6px; border-radius: 50%; background: var(--primary); box-shadow: 0 0 10px var(--primary); }
.spinner { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; border: 3px solid rgba(255, 255, 255, 0.1); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; display: none; }
.spinner.active { display: block; }
@keyframes spin { to { transform: translate(-50%, -50%) rotate(360deg); } }
.control-group { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 12px; }
.info-item { padding: 10px 12px; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border); border-radius: 8px; font-size: 11px; }
.info-value { color: var(--primary); font-weight: 600; font-family: 'Orbitron', sans-serif; }
@media (max-width: 1024px) { .app { grid-template-columns: 1fr; grid-template-rows: auto 1fr; } .panel { border-right: none; border-bottom: 1px solid var(--border); max-height: 50vh; } }""",

    # 3. JavaScript 邏輯
    f"{PROJECT_NAME}/assets/js/main.js": r"""import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const canvas = document.getElementById("c");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x1e1b4b, 10, 50);

const camera = new THREE.PerspectiveCamera(50, 1, 0.01, 2000);
camera.position.set(2, 1.5, 2.5);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);
const mainLight = new THREE.DirectionalLight(0xffffff, 1.2);
mainLight.position.set(5, 10, 5);
mainLight.castShadow = true;
mainLight.shadow.mapSize.width = 2048; mainLight.shadow.mapSize.height = 2048;
scene.add(mainLight);
const fillLight = new THREE.DirectionalLight(0x7c3aed, 0.3);
fillLight.position.set(-5, 5, -5); scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0x00d4ff, 0.5);
rimLight.position.set(0, 5, -10); scene.add(rimLight);

const gridHelper = new THREE.GridHelper(20, 20, 0x00d4ff, 0x7c3aed);
gridHelper.material.opacity = 0.2; gridHelper.material.transparent = true;
scene.add(gridHelper);

const elements = {
  fileInput: document.getElementById("file"), fileLabel: document.getElementById("fileLabel"),
  btnReset: document.getElementById("btnReset"), btnPlay: document.getElementById("btnPlay"), btnStop: document.getElementById("btnStop"),
  clipSelect: document.getElementById("clipSelect"), speed: document.getElementById("speed"), speedVal: document.getElementById("speedVal"),
  status: document.getElementById("status"), btnUpload: document.getElementById("btnUpload"), apiUrl: document.getElementById("apiUrl"),
  spinner: document.getElementById("spinner"), chipInfo: document.getElementById("chipInfo"), chipAnim: document.getElementById("chipAnim"),
  chipSkinned: document.getElementById("chipSkinned"), infoName: document.getElementById("infoName"), infoAnims: document.getElementById("infoAnims"),
  infoSkinned: document.getElementById("infoSkinned"), infoMeshes: document.getElementById("infoMeshes")
};

let state = { currentRoot: null, mixer: null, currentAction: null, currentClips: [], currentFile: null, meshCount: 0 };
const loader = new GLTFLoader();

function setStatus(msg, type = 'default') {
  elements.status.textContent = msg; elements.status.className = 'status';
  if (type !== 'default') elements.status.classList.add(type);
}
function showSpinner(show) { elements.spinner.classList.toggle('active', show); }
function updateInfo() {
  elements.infoName.textContent = state.currentFile?.name || '-'; elements.infoAnims.textContent = state.currentClips.length || '0';
  elements.infoSkinned.textContent = detectSkinned(state.currentRoot) ? '是' : '否'; elements.infoMeshes.textContent = state.meshCount || '0';
}
function clearCurrent() {
  if (state.currentAction) { state.currentAction.stop(); state.currentAction = null; }
  if (state.mixer) { state.mixer.stopAllAction(); state.mixer = null; }
  if (state.currentRoot) {
    scene.remove(state.currentRoot);
    state.currentRoot.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) { if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose()); else obj.material.dispose(); }
    });
    state.currentRoot = null;
  }
  state.currentClips = []; state.currentFile = null; state.meshCount = 0;
  elements.clipSelect.innerHTML = '<option>等待載入模型...</option>'; elements.clipSelect.disabled = true;
  elements.btnPlay.disabled = true; elements.btnStop.disabled = true; elements.btnReset.disabled = true; elements.speed.disabled = true; elements.btnUpload.disabled = true;
  elements.chipInfo.textContent = "未載入模型"; elements.chipAnim.textContent = "動畫: 無"; elements.chipSkinned.textContent = "骨架: 無"; updateInfo();
}
function frameObject(object3d) {
  const box = new THREE.Box3().setFromObject(object3d);
  const size = box.getSize(new THREE.Vector3()); const center = box.getCenter(new THREE.Vector3());
  object3d.position.sub(center); const box2 = new THREE.Box3().setFromObject(object3d); object3d.position.y -= box2.min.y;
  const maxDim = Math.max(size.x, size.y, size.z); const fov = camera.fov * (Math.PI / 180);
  let cameraZ = Math.abs(maxDim / (2 * Math.tan(fov / 2))); cameraZ *= 1.8;
  camera.position.set(cameraZ, cameraZ * 0.6, cameraZ); camera.near = Math.max(0.01, maxDim / 1000); camera.far = Math.max(2000, maxDim * 20);
  camera.updateProjectionMatrix(); controls.target.set(0, maxDim * 0.4, 0); controls.update();
}
function detectSkinned(root) { if (!root) return false; let skinned = false; root.traverse(obj => { if (obj.isSkinnedMesh) skinned = true; }); return skinned; }
function populateClips(clips) {
  elements.clipSelect.innerHTML = "";
  if (!clips || clips.length === 0) { elements.clipSelect.innerHTML = '<option>無可用動畫</option>'; elements.clipSelect.disabled = true; elements.btnPlay.disabled = true; elements.btnStop.disabled = true; elements.chipAnim.textContent = "動畫: 無"; return; }
  clips.forEach((c, i) => { const opt = document.createElement("option"); opt.value = String(i); opt.textContent = c.name || `動畫片段 ${i + 1}`; elements.clipSelect.appendChild(opt); });
  elements.clipSelect.disabled = false; elements.btnPlay.disabled = false; elements.btnStop.disabled = false; elements.speed.disabled = false; elements.chipAnim.textContent = `動畫: ${clips.length} 個片段`;
}
async function loadGltfFromUrl(url, fileName, isBlob = false) {
  try {
    const gltf = await loader.loadAsync(url);
    state.currentRoot = gltf.scene;
    state.currentRoot.traverse(obj => { if (obj.isMesh) { obj.castShadow = true; obj.receiveShadow = true; } });
    scene.add(state.currentRoot); frameObject(state.currentRoot);
    state.meshCount = 0; state.currentRoot.traverse(obj => { if (obj.isMesh) state.meshCount++; });
    const skinned = detectSkinned(state.currentRoot); elements.chipSkinned.textContent = "骨架: " + (skinned ? "已綁定" : "未綁定");
    state.currentClips = gltf.animations || [];
    if (state.currentClips.length > 0) { state.mixer = new THREE.AnimationMixer(state.currentRoot); populateClips(state.currentClips); playAnimation(0); } else { setStatus("模型載入成功（無動畫）", 'success'); }
    elements.btnReset.disabled = false; elements.btnUpload.disabled = false; elements.chipInfo.textContent = `模型: ${fileName}`; updateInfo();
  } catch (err) { console.error(err); setStatus("載入失敗", 'error'); }
}
function playAnimation(index) {
  if (!state.mixer || !state.currentClips[index]) return;
  if (state.currentAction) state.currentAction.stop();
  state.currentAction = state.mixer.clipAction(state.currentClips[index]); state.currentAction.reset(); state.currentAction.play();
  elements.btnPlay.textContent = "⏸️ 暫停"; setStatus(`播放中: ${state.currentClips[index].name || 'Animation'}`, 'success');
}
elements.fileInput.addEventListener("change", (e) => {
  const file = e.target.files?.[0]; if (!file) return;
  clearCurrent(); setStatus("載入中...", 'loading'); showSpinner(true); elements.fileLabel.textContent = `📁 ${file.name}`; state.currentFile = file;
  const url = URL.createObjectURL(file); loadGltfFromUrl(url, file.name).finally(() => { showSpinner(false); URL.revokeObjectURL(url); });
});
elements.btnUpload.addEventListener("click", async () => {
  if (!state.currentFile) return;
  const apiBase = elements.apiUrl.value.trim();
  if (!apiBase) { setStatus("請輸入 API 網址", 'error'); alert("請輸入 Google Colab 產生的 Ngrok 網址！"); return; }
  const endpoint = apiBase.replace(/\/$/, "") + "/api/rig";
  setStatus("正在上傳至雲端進行綁骨...", 'loading'); showSpinner(true); elements.btnUpload.disabled = true;
  const formData = new FormData(); formData.append('file', state.currentFile);
  try {
    const response = await fetch(endpoint, { method: 'POST', body: formData });
    if (!response.ok) throw new Error(`Server Error: ${response.status}`);
    const blob = await response.blob(); const riggedFile = new File([blob], `rigged_${state.currentFile.name}`, { type: 'model/gltf-binary' });
    clearCurrent(); const url = URL.createObjectURL(riggedFile); await loadGltfFromUrl(url, riggedFile.name);
    const helper = new THREE.SkeletonHelper(state.currentRoot); scene.add(helper);
    state.currentFile = riggedFile; elements.chipSkinned.textContent = "骨架: 自動生成 (Server)"; setStatus("自動綁骨完成！", 'success');
  } catch (err) { console.error(err); setStatus("處理失敗: " + err.message, 'error'); } finally { showSpinner(false); elements.btnUpload.disabled = false; }
});
elements.btnReset.addEventListener("click", () => { if (state.currentRoot) { frameObject(state.currentRoot); setStatus("視角已重置", 'success'); } });
elements.btnPlay.addEventListener("click", () => { if (!state.mixer) return; if (state.mixer.timeScale === 0) { state.mixer.timeScale = Number(elements.speed.value); elements.btnPlay.textContent = "⏸️ 暫停"; } else { state.mixer.timeScale = 0; elements.btnPlay.textContent = "▶️ 播放"; } });
elements.btnStop.addEventListener("click", () => { if (state.currentAction) { state.currentAction.stop(); state.mixer.timeScale = 0; elements.btnPlay.textContent = "▶️ 播放"; } });
elements.clipSelect.addEventListener("change", (e) => { state.mixer.timeScale = Number(elements.speed.value); playAnimation(Number(e.target.value)); });
elements.speed.addEventListener("input", (e) => { const val = Number(e.target.value); elements.speedVal.textContent = val.toFixed(2) + "x"; if (state.mixer && state.mixer.timeScale !== 0) { state.mixer.timeScale = val; } });
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const w = canvas.parentElement.clientWidth; const h = canvas.parentElement.clientHeight;
  if (canvas.width !== w || canvas.height !== h) { renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  controls.update(); if (state.mixer) state.mixer.update(clock.getDelta()); renderer.render(scene, camera);
}
animate();""",

    # 4. Blender 腳本
    f"{PROJECT_NAME}/backend/auto_rig.py": r"""import bpy
import sys
bpy.ops.wm.read_factory_settings(use_empty=True)
argv = sys.argv
try:
    argv = argv[argv.index("--") + 1:] 
    input_path = argv[0]
    output_path = argv[1]
except:
    print("Error: 請提供輸入和輸出路徑")
    sys.exit(1)
print(f"Blender: 正在處理 {input_path}")
try:
    bpy.ops.import_scene.gltf(filepath=input_path)
    mesh_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break
    if mesh_obj:
        print(f"Blender: 找到網格 {mesh_obj.name}")
        bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
        armature = bpy.context.object
        armature.name = "AutoRig_Armature"
        dim = mesh_obj.dimensions
        armature.scale = (dim.z/2, dim.z/2, dim.z/2)
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    bpy.ops.export_scene.gltf(filepath=output_path)
    print("Blender: 匯出成功")
except Exception as e:
    print(f"Blender Error: {e}")
    sys.exit(1)""",

    # 5. README
    f"{PROJECT_NAME}/README.md": r"""# Web Rig Studio
一個基於 Web 的 3D 模型查看器，整合了自動綁骨架功能。

## 如何執行
1. 安裝 VS Code 外掛 "Live Server"。
2. 對 `index.html` 按右鍵 -> "Open with Live Server"。
3. 後端功能請參考 `backend/auto_rig.py` 搭配 Google Colab 使用。
"""
}

# 執行檔案寫入
print(f"🚀 正在建立專案: {PROJECT_NAME} ...")

for path, content in files.items():
    # 建立資料夾
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # 寫入檔案
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已建立: {path}")

print("\n🎉 專案建立完成！請進入 web-rig-studio 資料夾開始使用。")
