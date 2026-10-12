// extrude: an SVG logo or shape, extruded and turning slowly under soft studio light.
// Shot: { three: "three/extrude.js", params: {
//   svg: "logo.svg",              path relative to work/; filled shapes are extruded (strokes are ignored)
//   color: "#…",                  one colour for every shape (default: each shape keeps its SVG fill)
//   background: "#…",             default --ink
//   depth: 0.18,                  extrusion depth as a share of the shape's width
//   size: 0.62,                   share of the frame's short side the shape fills
//   turn: [-25, 20], tilt: 12,    yaw in degrees over the shot (linear, so it never reads as frozen), and pitch
//   intro: 0.6 } }                seconds the shape takes to grow in (0: there from the first frame)
import * as THREE from "./three.module.min.js";
import { SVGLoader } from "./SVGLoader.js";

const rad = (d) => (d * Math.PI) / 180;
const outCubic = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);

function read(url) {
  // fetch() can't read file:// pages; XHR can (capture runs Chromium with --allow-file-access-from-files)
  return new Promise((ok, fail) => {
    const x = new XMLHttpRequest();
    x.open("GET", url);
    x.onload = () => (x.responseText ? ok(x.responseText) : fail(new Error(`${url} is empty or unreadable`)));
    x.onerror = () => fail(new Error(`cannot read ${url}`));
    x.send();
  });
}

export async function create(canvas, params, { width, height, css }) {
  if (!params.svg) throw new Error("extrude needs params.svg");
  const data = new SVGLoader().parse(await read(new URL(params.svg, location.href).href));
  const shapes = [];
  for (const path of data.paths) {
    const fill = path.userData?.style?.fill;
    if (!fill || fill === "none") continue;
    for (const shape of SVGLoader.createShapes(path)) shapes.push({ shape, color: path.color });
  }
  if (!shapes.length) throw new Error(`${params.svg} has no filled shapes to extrude`);
  const box = new THREE.Box2();
  for (const { shape } of shapes) for (const p of shape.getPoints(24)) box.expandByPoint(p);
  const w = box.max.x - box.min.x, h = box.max.y - box.min.y, depth = (params.depth ?? 0.18) * w;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height, false);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(params.background || css("--ink") || "#111827");

  // SVG y runs down: flip it, centre the shape, and push it back by half its depth so it turns about its middle
  const logo = new THREE.Group(), inner = new THREE.Group();
  shapes.forEach(({ shape, color }, i) => {
    const geo = new THREE.ExtrudeGeometry(shape, {
      depth, curveSegments: 32, bevelEnabled: true, bevelThickness: depth * 0.12, bevelSize: Math.min(w, h) * 0.012, bevelSegments: 4,
    });
    const mat = new THREE.MeshStandardMaterial({
      color: params.color ? new THREE.Color(params.color) : color, metalness: 0.1, roughness: 0.42, side: THREE.DoubleSide,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.z = i * depth * 0.05;  // a later SVG shape sits on top: lift it, or coplanar faces shimmer
    inner.add(mesh);
  });
  inner.scale.set(1, -1, 1);
  inner.position.set(-(box.min.x + w / 2), box.min.y + h / 2, -depth / 2);
  logo.add(inner);
  const unit = 1 / Math.max(w, h);
  logo.scale.setScalar(unit);
  scene.add(logo);

  scene.add(new THREE.HemisphereLight(0xffffff, 0x404040, 1.5));
  const key = new THREE.DirectionalLight(0xffffff, 2.9);
  key.position.set(2, 3, 4);
  const rim = new THREE.DirectionalLight(0xffffff, 1.6);
  rim.position.set(-3, 1, -3);
  scene.add(key, rim);

  // fit: the shape's larger side fills `size` of the frame's short side
  const camera = new THREE.PerspectiveCamera(28, width / height, 0.01, 100);
  const visible = (params.size ?? 0.62) * Math.min(width, height) / height;  // share of the frame height
  const dist = 1 / (visible * 2 * Math.tan(rad(camera.fov) / 2));
  camera.position.set(0, 0, dist);
  camera.lookAt(0, 0, 0);
  const [y0, y1] = params.turn || [-25, 20], tilt = params.tilt ?? 12, intro = params.intro ?? 0.6;

  return {
    render(t, p = 0) {
      const grow = intro > 0 ? 0.82 + 0.18 * outCubic(t / intro) : 1;
      logo.scale.setScalar(unit * grow);
      logo.rotation.set(rad(tilt), rad(y0 + (y1 - y0) * p), 0);
      renderer.render(scene, camera);
      return {};
    },
  };
}
