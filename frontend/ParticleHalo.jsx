// ParticleHalo.jsx
// MZ/X – Neon Partikula Aura az AI Core körül

import React, { useMemo, useRef } from "react";
import { Points, PointMaterial } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";

export default function ParticleHalo({ vol = 0.02 }) {
  const ref = useRef();
  const radius = 3;

  // Partikula pozíciók generálása
  const particles = useMemo(() => {
    const arr = [];
    for (let i = 0; i < 500; i++) {
      const r = radius + Math.random() * 0.5;
      const angle = Math.random() * Math.PI * 2;
      arr.push([
        Math.cos(angle) * r,
        (Math.random() - 0.5) * 1.5,
        Math.sin(angle) * r,
      ]);
    }
    return new Float32Array(arr.flat());
  }, []);

  // Animáció: lassú forgás + pulzálás a volatilitással
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    ref.current.rotation.y = t * 0.1;
    ref.current.scale.set(1 + vol * 4, 1 + vol * 4, 1 + vol * 4);
  });

  return (
    <group ref={ref}>
      <Points positions={particles} stride={3}>
        <PointMaterial
          transparent
          opacity={0.9}
          size={0.04}
          sizeAttenuation
          color="#ff00ff"
          depthWrite={false}
        />
      </Points>
    </group>
  );
}
