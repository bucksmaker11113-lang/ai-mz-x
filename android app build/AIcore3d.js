// components/AICore3D.js
// MZ/X ANDROID – Natív 3D AI Core (Expo + ThreeJS + React Native)
// Ez mobilon futó THREE.js holografikus mag

import React, { useRef } from 'react';
import { GLView } from 'expo-gl';
import { Renderer } from 'expo-three';
import * as THREE from 'three';

export default function AICore3D() {
  const rotationRef = useRef(0);

  return (
    <GLView
      style={{ width: '100%', height: '100%' }}
      onContextCreate={async (gl) => {
        const { drawingBufferWidth: width, drawingBufferHeight: height } = gl;

        // THREE renderer létrehozása
        const renderer = new Renderer({ gl });
        renderer.setSize(width, height);

        // Szcéna
        const scene = new THREE.Scene();

        // Kamera
        const camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 100);
        camera.position.z = 4;

        // Fények
        const ambient = new THREE.AmbientLight(0xffffff, 0.4);
        scene.add(ambient);

        const point = new THREE.PointLight(0xff00ff, 1.6);
        point.position.set(5, 5, 5);
        scene.add(point);

        // AI Core belső holografikus gömb
        const sphereGeo = new THREE.SphereGeometry(1, 64, 64);
        const sphereMat = new THREE.MeshStandardMaterial({
          color: new THREE.Color('#bb00ff'),
          emissive: new THREE.Color('#ff00ff'),
          emissiveIntensity: 2.5,
          metalness: 0.6,
          roughness: 0.2,
        });

        const sphere = new THREE.Mesh(sphereGeo, sphereMat);
        scene.add(sphere);

        // Külső neon toruszgyűrű
        const torusGeo = new THREE.TorusGeometry(1.6, 0.08, 16, 200);
        const torusMat = new THREE.MeshStandardMaterial({
          color: new THREE.Color('#00c6ff'),
          emissive: new THREE.Color('#00c6ff'),
          emissiveIntensity: 3.2,
          metalness: 0.6,
          roughness: 0.15,
        });

        const torus = new THREE.Mesh(torusGeo, torusMat);
        scene.add(torus);

        // Animációs ciklus
        const animate = () => {
          rotationRef.current += 0.01;
          sphere.rotation.y += 0.01;
          torus.rotation.x += 0.015;
          torus.rotation.y += 0.01;

          renderer.render(scene, camera);
          gl.endFrameEXP();
          requestAnimationFrame(animate);
        };

        animate();
      }}
    />
  );
}
