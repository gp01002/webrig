import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// 初始化 Three.js
const canvas = document.getElementById("c");
const renderer = new THREE.WebGLRenderer({ 
  canvas, 
  antialias: true, 
  alpha: true,
  powerPreference: "high-performance"
});
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

// 燈光設置
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

const mainLight = new THREE.DirectionalLight(0xffffff, 1.2);
mainLight.position.set(5, 10, 5);
mainLight.castShadow = true;
mainLight.shadow.mapSize.width = 2048;
mainLight.shadow.mapSize.height = 2048;
scene.add(mainLight);

const fillLight = new THREE.DirectionalLight(0x7c3aed, 0.3);
fillLight.position.set(-5, 5, -5);
scene.add(fillLight);

const rimLight = new THREE.DirectionalLight(0x00d4ff, 0.5);
rimLight.position.set(0, 5, -10);
scene.add(rimLight);

// 地面網格
const gridHelper = new THREE.GridHelper(20, 20, 0x00d4ff, 0x7c3aed);
gridHelper.material.opacity = 0.2;
gridHelper.material.transparent = true;
scene.add(gridHelper);

// UI 元素
const elements = {
  fileInput: document.getElementById("file"),
  fileLabel: document.getElementById("fileLabel"),
  btnReset: document.getElementById("btnReset"),
  btnPlay: document.getElementById("btnPlay"),
  btnStop: document.getElementById("btnStop"),
  clipSelect: document.getElementById("clipSelect"),
  speed: document.getElementById("speed"),
  speedVal: document.getElementById("speedVal"),
  status: document.getElementById("status"),
  btnUpload: document.getElementById("btnUpload"),
  apiUrl: document.getElementById("apiUrl"),
  spinner: document.getElementById("spinner"),
  chipInfo: document.getElementById("chipInfo"),
  chipAnim: document.getElementById("chipAnim"),
  chipSkinned: document.getElementById("chipSkinned"),
  infoName: document.getElementById("infoName"),
  infoAnims: document.getElementById("infoAnims"),
  infoSkinned: document.getElementById("infoSkinned"),
  infoMeshes: document.getElementById("infoMeshes")
};

// 狀態管理
let state = {
  currentRoot: null,
  mixer: null,
  currentAction: null,
  currentClips: [],
  currentFile: null,
  meshCount: 0
};

const loader = new GLTFLoader();

// 輔助函式
function setStatus(msg, type = 'default') {
  elements.status.textContent = msg;
  elements.status.className = 'status';
  if (type !== 'default') elements.status.classList.add(type);
}

function showSpinner(show) {
  elements.spinner.classList.toggle('active', show);
}

function updateInfo() {
  elements.infoName.textContent = state.currentFile?.name || '-';
  elements.infoAnims.textContent = state.currentClips.length || '0';
  elements.infoSkinned.textContent = detectSkinned(state.currentRoot) ? '是' : '否';
  elements.infoMeshes.textContent = state.meshCount || '0';
}

function clearCurrent() {
  if (state.currentAction) {
    state.currentAction.stop();
    state.currentAction = null;
  }
  if (state.mixer) {
    state.mixer.stopAllAction();
    state.mixer = null;
  }
  if (state.currentRoot) {
    scene.remove(state.currentRoot);
    state.currentRoot.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
        else obj.material.dispose();
      }
    });
    state.currentRoot = null;
  }

  state.currentClips = [];
  state.currentFile = null;
  state.meshCount = 0;

  elements.clipSelect.innerHTML = '<option>等待載入模型...</option>';
  elements.clipSelect.disabled = true;
  elements.btnPlay.disabled = true;
  elements.btnStop.disabled = true;
  elements.btnReset.disabled = true;
  elements.speed.disabled = true;
  elements.btnUpload.disabled = true;

  elements.chipInfo.textContent = "未載入模型";
  elements.chipAnim.textContent = "動畫: 無";
  elements.chipSkinned.textContent = "骨架: 無";

  updateInfo();
}

function frameObject(object3d) {
  const box = new THREE.Box3().setFromObject(object3d);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());

  object3d.position.sub(center);
  const box2 = new THREE.Box3().setFromObject(object3d);
  object3d.position.y -= box2.min.y; // 貼地

  const maxDim = Math.max(size.x, size.y, size.z);
  const fov = camera.fov * (Math.PI / 180);
  let cameraZ = Math.abs(maxDim / (2 * Math.tan(fov / 2)));
  cameraZ *= 1.8;

  camera.position.set(cameraZ, cameraZ * 0.6, cameraZ);
  camera.near = Math.max(0.01, maxDim / 1000);
  camera.far = Math.max(2000, maxDim * 20);
  camera.updateProjectionMatrix();

  controls.target.set(0, maxDim * 0.4, 0);
  controls.update();
}

function detectSkinned(root) {
  if (!root) return false;
  let skinned = false;
  root.traverse(obj => {
    if (obj.isSkinnedMesh) skinned = true;
  });
  return skinned;
}

function populateClips(clips) {
  elements.clipSelect.innerHTML = "";
  if (!clips || clips.length === 0) {
    elements.clipSelect.innerHTML = '<option>無可用動畫</option>';
    elements.clipSelect.disabled = true;
    elements.btnPlay.disabled = true;
    elements.btnStop.disabled = true;
    elements.chipAnim.textContent = "動畫: 無";
    return;
  }

  clips.forEach((c, i) => {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = c.name || `動畫片段 ${i + 1}`;
    elements.clipSelect.appendChild(opt);
  });

  elements.clipSelect.disabled = false;
  elements.btnPlay.disabled = false;
  elements.btnStop.disabled = false;
  elements.speed.disabled = false;
  elements.chipAnim.textContent = `動畫: ${clips.length} 個片段`;
}

// 載入處理邏輯
async function loadGltfFromUrl(url, fileName, isBlob = false) {
  try {
    const gltf = await loader.loadAsync(url);
    
    state.currentRoot = gltf.scene;
    state.currentRoot.traverse(obj => {
      if (obj.isMesh) {
        obj.castShadow = true;
        obj.receiveShadow = true;
      }
    });

    scene.add(state.currentRoot);
    frameObject(state.currentRoot);

    // 統計資料
    state.meshCount = 0;
    state.currentRoot.traverse(obj => { if (obj.isMesh) state.meshCount++; });
    
    const skinned = detectSkinned(state.currentRoot);
    elements.chipSkinned.textContent = "骨架: " + (skinned ? "已綁定" : "未綁定");

    // 動畫
    state.currentClips = gltf.animations || [];
    if (state.currentClips.length > 0) {
      state.mixer = new THREE.AnimationMixer(state.currentRoot);
      populateClips(state.currentClips);
      playAnimation(0);
    } else {
      setStatus("模型載入成功（無動畫）", 'success');
    }

    elements.btnReset.disabled = false;
    elements.btnUpload.disabled = false;
    
    elements.chipInfo.textContent = `模型: ${fileName}`;
    updateInfo();

  } catch (err) {
    console.error(err);
    setStatus("載入失敗", 'error');
  }
}

function playAnimation(index) {
  if (!state.mixer || !state.currentClips[index]) return;
  
  if (state.currentAction) state.currentAction.stop();
  state.currentAction = state.mixer.clipAction(state.currentClips[index]);
  state.currentAction.reset();
  state.currentAction.play();
  
  elements.btnPlay.textContent = "⏸️ 暫停";
  setStatus(`播放中: ${state.currentClips[index].name || 'Animation'}`, 'success');
}

// === 事件監聽 ===

// 1. 檔案上傳
elements.fileInput.addEventListener("change", (e) => {
  const file = e.target.files?.[0];
  if (!file) return;

  clearCurrent();
  setStatus("載入中...", 'loading');
  showSpinner(true);
  elements.fileLabel.textContent = `📁 ${file.name}`;
  state.currentFile = file;

  const url = URL.createObjectURL(file);
  loadGltfFromUrl(url, file.name).finally(() => {
    showSpinner(false);
    URL.revokeObjectURL(url);
  });
});

// 2. 自動綁骨 (API)
elements.btnUpload.addEventListener("click", async () => {
  if (!state.currentFile) return;
  
  const apiBase = elements.apiUrl.value.trim();
  if (!apiBase) {
    setStatus("請輸入 API 網址", 'error');
    alert("請輸入 Google Colab 產生的 Ngrok 網址！");
    return;
  }

  const endpoint = apiBase.replace(/\/$/, "") + "/api/rig";

  setStatus("正在上傳至雲端進行綁骨 (約需 10-30 秒)...", 'loading');
  showSpinner(true);
  elements.btnUpload.disabled = true;

  const formData = new FormData();
  formData.append('file', state.currentFile);

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error(`Server Error: ${response.status}`);

    const blob = await response.blob();
    const riggedFile = new File([blob], `rigged_${state.currentFile.name}`, { type: 'model/gltf-binary' });
    
    clearCurrent();
    
    // 載入回傳的模型
    const url = URL.createObjectURL(riggedFile);
    await loadGltfFromUrl(url, riggedFile.name);
    
    // 顯示骨架輔助線
    const helper = new THREE.SkeletonHelper(state.currentRoot);
    scene.add(helper);
    
    state.currentFile = riggedFile;
    elements.chipSkinned.textContent = "骨架: 自動生成 (Server)";
    setStatus("自動綁骨完成！", 'success');
    
  } catch (err) {
    console.error(err);
    setStatus("處理失敗: " + err.message, 'error');
  } finally {
    showSpinner(false);
    elements.btnUpload.disabled = false;
  }
});

// 3. 其他控制項
elements.btnReset.addEventListener("click", () => {
  if (state.currentRoot) {
    frameObject(state.currentRoot);
    setStatus("視角已重置", 'success');
  }
});

elements.btnPlay.addEventListener("click", () => {
  if (!state.mixer) return;
  if (state.mixer.timeScale === 0) {
    state.mixer.timeScale = Number(elements.speed.value);
    elements.btnPlay.textContent = "⏸️ 暫停";
  } else {
    state.mixer.timeScale = 0;
    elements.btnPlay.textContent = "▶️ 播放";
  }
});

elements.btnStop.addEventListener("click", () => {
  if (state.currentAction) {
    state.currentAction.stop();
    state.mixer.timeScale = 0;
    elements.btnPlay.textContent = "▶️ 播放";
  }
});

elements.clipSelect.addEventListener("change", (e) => {
  state.mixer.timeScale = Number(elements.speed.value);
  playAnimation(Number(e.target.value));
});

elements.speed.addEventListener("input", (e) => {
  const val = Number(e.target.value);
  elements.speedVal.textContent = val.toFixed(2) + "x";
  if (state.mixer && state.mixer.timeScale !== 0) {
    state.mixer.timeScale = val;
  }
});

// 4. 渲染循環
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  
  // Resize
  const w = canvas.parentElement.clientWidth;
  const h = canvas.parentElement.clientHeight;
  if (canvas.width !== w || canvas.height !== h) {
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  
  controls.update();
  if (state.mixer) state.mixer.update(clock.getDelta());
  renderer.render(scene, camera);
}

animate();