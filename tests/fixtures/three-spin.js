// test fixture for three shots: a lit cube turning with t in the brand accent, plus one anchor above it
import * as THREE from "./three.module.min.js";

export async function create(canvas, params, { width, height, css }) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height, false);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(css("--ink"));
  const camera = new THREE.PerspectiveCamera(35, width / height, 0.1, 100);
  camera.position.set(0, 0, 6);
  const cube = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.4, 1.4), new THREE.MeshStandardMaterial({ color: css("--accent") }));
  const key = new THREE.DirectionalLight(0xffffff, 2.5);
  key.position.set(3, 4, 5);
  scene.add(cube, key, new THREE.AmbientLight(0xffffff, 0.8));
  const top = new THREE.Vector3(0, 1.2, 0);
  return {
    render(t) {
      cube.rotation.set(0.4 + t * 0.6, t * 1.1, 0);
      renderer.render(scene, camera);
      const v = top.clone().project(camera);
      return { anchors: { top: [(v.x + 1) / 2 * width, (1 - v.y) / 2 * height, 1] } };
    },
  };
}
