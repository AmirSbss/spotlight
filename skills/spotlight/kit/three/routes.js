// routes: a dotted globe (or flat map) with points that pop in and great-circle routes that draw in.
// Shot: { three: "three/routes.js", params: {
//   view: "globe" | "flat",                       default globe
//   points: [{ id, lat, lon, at }],               at: seconds into the shot when the point pops in (default 0)
//   routes: [{ from, to, at, dur }],              point ids; draws from `at` over `dur` (default 1.2 s)
//   center: [lat, lon] | { from: [lat, lon], to: [lat, lon] },   default: the points' centre, drifting 16° east
//   zoom: 1,                                      >1 moves in
//   colors: { land, ocean, route, point } } }     default: --paper, --ink, --accent, --accent
// Anchors: every point id -> its screen position; on the globe a point turning away fades out, so its label hides.
// Everything is a function of t: the camera moves at a near-constant speed, so the shot never reads as frozen.
import * as THREE from "./three.module.min.js";
import { landDots } from "./land-dots.js";

const rad = (d) => (d * Math.PI) / 180;
const clamp = (x, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, x));
const outCubic = (x) => 1 - Math.pow(1 - x, 3);
const inOutCubic = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const outBack = (x) => 1 + 2.2 * Math.pow(x - 1, 3) + 1.2 * Math.pow(x - 1, 2);

// colours mix the way a designer means it, in sRGB: a linear-light mix of near-black and white comes out grey
const mix = (a, b, k) => a.clone().convertLinearToSRGB().lerp(b.clone().convertLinearToSRGB(), k).convertSRGBToLinear();

// lat/lon on the unit sphere: y up, (0, 0) facing +z
function sphere(lat, lon, r = 1) {
  const p = rad(lat), l = rad(lon);
  return new THREE.Vector3(r * Math.cos(p) * Math.sin(l), r * Math.sin(p), r * Math.cos(p) * Math.cos(l));
}
// lat/lon on the flat map: 4 x 2 units, equirectangular
const plane = (lat, lon, z = 0) => new THREE.Vector3((lon / 180) * 2, (lat / 90) * 1, z);

function roundDot() {
  // a round sprite for the land dots (points are squares otherwise)
  const c = document.createElement("canvas");
  c.width = c.height = 64;
  const g = c.getContext("2d");
  g.fillStyle = "#fff";
  g.beginPath();
  g.arc(32, 32, 28, 0, Math.PI * 2);
  g.fill();
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

export async function create(canvas, params, { width, height, css }) {
  const flat = params.view === "flat";
  const col = (v, fallback) => new THREE.Color(v || css(fallback) || "#ffffff");
  const colors = params.colors || {};
  const land = col(colors.land, "--paper"), ink = col(colors.ocean, "--ink");
  const route = col(colors.route, "--accent"), pointCol = col(colors.point, "--accent");

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height, false);
  const scene = new THREE.Scene();
  scene.background = ink;
  const camera = new THREE.PerspectiveCamera(30, width / height, 0.01, 100);
  const world = new THREE.Group();
  scene.add(world);

  const pts = params.points || [];
  const byId = Object.fromEntries(pts.map((p) => [p.id, p]));
  const at = (lat, lon, lift = 0) => (flat ? plane(lat, lon, lift) : sphere(lat, lon, 1 + lift));

  // land dots, and on the globe an ocean sphere that hides the far side, with a faint rim
  const ll = landDots(), pos = new Float32Array((ll.length / 2) * 3);
  for (let i = 0; i < ll.length / 2; i++) at(ll[2 * i], ll[2 * i + 1]).toArray(pos, 3 * i);
  const dotsGeo = new THREE.BufferGeometry();
  dotsGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const dots = new THREE.Points(dotsGeo, new THREE.PointsMaterial({
    color: land, size: flat ? 0.022 : 0.0125, map: roundDot(), alphaTest: 0.5, transparent: false, opacity: 1,
  }));
  dots.material.color = mix(land, ink, 0.45);
  world.add(dots);
  let rim = null;
  if (!flat) {
    const ocean = new THREE.Mesh(new THREE.SphereGeometry(0.996, 96, 64), new THREE.MeshBasicMaterial({ color: mix(ink, land, 0.06) }));
    world.add(ocean);
    rim = new THREE.Mesh(new THREE.RingGeometry(1.0, 1.014, 160), new THREE.MeshBasicMaterial({ color: route, transparent: true, opacity: 0.32 }));
    scene.add(rim);  // in the scene, not the world: it always faces the camera
  }

  // points: a solid dot that pops in, and a ring that pulses outward
  const marks = pts.map((p) => {
    const g = new THREE.Group();
    const dot = new THREE.Mesh(new THREE.CircleGeometry(flat ? 0.018 : 0.017, 32), new THREE.MeshBasicMaterial({ color: pointCol }));
    const ring = new THREE.Mesh(new THREE.RingGeometry(flat ? 0.022 : 0.021, flat ? 0.028 : 0.027, 48),
      new THREE.MeshBasicMaterial({ color: pointCol, transparent: true, side: THREE.DoubleSide }));
    g.add(dot, ring);
    const where = at(p.lat, p.lon, flat ? 0.002 : 0.004);
    g.position.copy(where);
    if (!flat) g.lookAt(where.clone().multiplyScalar(2));  // lie on the surface
    world.add(g);
    return { p, g, dot, ring };
  });

  // routes: a great circle, lifted with distance, drawn in by growing the tube's index range
  const RADIAL = 8, SEGS = 160;
  const tubes = (params.routes || []).map((r) => {
    const a = byId[r.from], b = byId[r.to];
    if (!a || !b) throw new Error(`route ${r.from} -> ${r.to}: unknown point id`);
    const va = sphere(a.lat, a.lon), vb = sphere(b.lat, b.lon), angle = va.angleTo(vb);
    const lift = 0.06 + 0.32 * (angle / Math.PI);
    const path = [];
    for (let i = 0; i <= 96; i++) {
      const u = i / 96, v = new THREE.Vector3().copy(va).lerp(vb, u).normalize();
      if (angle > 1e-6) {  // slerp: lerp-and-normalise bunches points in the middle of long arcs
        const s = Math.sin(angle);
        v.copy(va).multiplyScalar(Math.sin((1 - u) * angle) / s).addScaledVector(vb, Math.sin(u * angle) / s);
      }
      const h = lift * Math.sin(Math.PI * u);
      if (flat) {
        const lat = 90 - (Math.acos(clamp(v.y, -1, 1)) * 180) / Math.PI;
        let lon = (Math.atan2(v.x, v.z) * 180) / Math.PI;
        if (path.length) {  // unwrap across the antimeridian so the arc doesn't jump
          const prev = path[path.length - 1].x * 90;
          while (lon - prev > 180) lon -= 360;
          while (prev - lon > 180) lon += 360;
        }
        path.push(plane(lat, lon, h * 0.9));
      } else {
        path.push(v.multiplyScalar(1 + h));
      }
    }
    const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(path), SEGS, flat ? 0.0075 : 0.0065, RADIAL, false);
    const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: route }));
    const head = new THREE.Mesh(new THREE.SphereGeometry(flat ? 0.013 : 0.012, 16, 12), new THREE.MeshBasicMaterial({ color: route }));
    world.add(mesh, head);
    return { r, geo, mesh, head, curve: geo.parameters.path };
  });

  // camera: centre eases from -> to at a near-constant speed
  const centroid = () => {
    const s = new THREE.Vector3();
    for (const p of pts) s.add(sphere(p.lat, p.lon));
    if (!pts.length || s.lengthSq() < 1e-9) return [20, 0];
    s.normalize();
    return [90 - (Math.acos(s.y) * 180) / Math.PI, (Math.atan2(s.x, s.z) * 180) / Math.PI];
  };
  const c0 = params.center ? (Array.isArray(params.center) ? params.center : params.center.from) : centroid();
  const c1 = params.center ? (Array.isArray(params.center) ? [c0[0], c0[1] + 10] : params.center.to)
    : [c0[0], c0[1] + 16];
  let dLon = c1[1] - c0[1];
  while (dLon > 180) dLon -= 360;
  while (dLon < -180) dLon += 360;
  const zoom = params.zoom || 1;
  const fit = Math.min(rad(camera.fov), 2 * Math.atan(Math.tan(rad(camera.fov) / 2) * camera.aspect)) / 2;
  const dist = flat ? 0 : 1 + (1 / Math.sin(fit * 0.9) - 1) / zoom;

  return {
    render(t, p = 0) {
      const e = 0.75 * p + 0.25 * inOutCubic(p);  // never stops: an eased move stalls at its ends and reads as frozen
      const lat = c0[0] + (c1[0] - c0[0]) * e, lon = c0[1] + dLon * e;
      if (flat) {
        const span = 2.6 / zoom;  // map units visible vertically
        const target = plane(lat, lon);
        camera.position.set(target.x, target.y - span * 0.32, span / (2 * Math.tan(rad(camera.fov) / 2)));
        camera.lookAt(target);
      } else {
        world.rotation.set(rad(lat), -rad(lon), 0, "XYZ");  // turn the globe so (lat, lon) faces the camera
        camera.position.set(0, 0, dist);
        camera.lookAt(0, 0, 0);
        rim.visible = zoom < 1.6;
      }
      const anchors = {};
      world.updateMatrixWorld(true);
      for (const m of marks) {
        const q = clamp((t - (m.p.at || 0)) / 0.35);
        m.g.scale.setScalar(Math.max(1e-3, outBack(q)));
        m.g.visible = q > 0;
        const k = ((t - (m.p.at || 0)) % 1.6 + 1.6) % 1.6 / 1.6;  // pulse every 1.6 s
        m.ring.scale.setScalar(1 + 1.6 * outCubic(k));
        m.ring.material.opacity = q > 0 ? 0.7 * (1 - k) : 0;
        const w = m.g.getWorldPosition(new THREE.Vector3());
        const facing = flat ? 1 : clamp((w.clone().normalize().dot(camera.position.clone().normalize()) - 0.12) / 0.18);
        const s = w.clone().project(camera);
        anchors[m.p.id] = [((s.x + 1) / 2) * width, ((1 - s.y) / 2) * height, facing * clamp(q * 2)];
      }
      for (const r of tubes) {
        const q = outCubic(clamp((t - (r.r.at || 0)) / (r.r.dur || 1.2)));
        const segs = Math.floor(q * SEGS);
        r.geo.setDrawRange(0, segs * RADIAL * 6);
        r.head.visible = q > 0 && q < 1;
        if (q > 0) r.head.position.copy(r.curve.getPoint(Math.max(q, 1e-3)));
      }
      renderer.render(scene, camera);
      return { anchors };
    },
  };
}
