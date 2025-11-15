// AICore3D.jsx
// MZ/X – Holografikus 3D AI Core (React Three Fiber + Drei)

import React, { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Sphere, Torus, OrbitControls } from "@react-three/drei";

function CoreInner({ trend, vol }) {
  const mesh = useRef();

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    const pulse = 1 + Math.sin(t * 2 + trend * 5) * 0.05;
    mesh.current.scale.set(pulse, pulse, pulse);
  });

  return (
    <Sphere args={[1, 64, 64]} ref={mesh}>
      <meshStandardMaterial
        color={trend > 0.55 ? "#00ffcc" : trend < 0.45 ? "#ff0066" : "#bb00ff"}
        emissive={trend > 0.55 ? "#00ffaa" : trend < 0.45 ? "#ff0044" : "#ff00ff"}
        emissiveIntensity={2.5 + vol * 5}
        metalness={0.6}
        roughness={0.2}
      />
    </Sphere>
  );
}

function CoreRing({ vol }) {
  const torusRef = useRef();

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    torusRef.current.rotation.x = t * 0.4;
    torusRef.current.rotation.y = t * 0.3;
    torusRef.current.scale.set(1 + vol * 4, 1 + vol * 4, 1 + vol * 4);
  });

  return (
    <Torus ref={torusRef} args={[1.6, 0.08, 16, 200]}>
      <meshStandardMaterial
        color="#00c6ff"
        emissive="#00c6ff"
        emissiveIntensity={4 + vol * 10}
        metalness={0.6}
        roughness={0.15}
      />
    </Torus>
  );
}

export default function AICore3D({ trend = 0.5, vol = 0.02 }) {
  return (
    <div style={{ width: "100%", height: "100%" }}>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={2} />

        <CoreInner trend={trend} vol={vol} />
        <CoreRing vol={vol} />

        <OrbitControls enableZoom={false} enablePan={false} />
      </Canvas>
    </div>
  );
}
