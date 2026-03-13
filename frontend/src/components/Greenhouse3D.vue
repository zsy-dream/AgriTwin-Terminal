<template>
  <div ref="container" class="relative w-full h-full min-h-0 rounded-xl overflow-hidden">
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
      <div class="text-center">
        <div class="relative h-12 w-12 mx-auto mb-2">
          <div class="absolute inset-0 rounded-full border-2 border-cyber-neonViolet/70 border-t-transparent animate-spin" />
        </div>
        <span class="text-xs text-slate-400">加载3D模型...</span>
      </div>
    </div>
    <div class="absolute top-2 left-2 z-10 flex gap-2">
      <span class="px-2 py-1 rounded-full bg-cyber-neonCyan/20 text-[10px] text-cyber-neonCyan">3D View</span>
      <span v-if="stageName" class="px-2 py-1 rounded-full bg-cyber-neonViolet/20 text-[10px] text-cyber-neonViolet">{{ stageName }}</span>
    </div>
    <div class="absolute bottom-2 right-2 z-10 flex gap-1">
      <button @click="resetCamera" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs" title="重置视角">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'

const props = defineProps({
  stageName: { type: String, default: '生长期' },
  dayProgress: { type: Number, default: 0.5 } // 0-1 生长进度
})

const container = ref(null)
const loading = ref(true)

let scene, camera, renderer, greenhouse, plant, animationId
let rotateSpeed = 0.005

const init = () => {
  if (!container.value) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight || 200

  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x0a0a1a)
  scene.fog = new THREE.Fog(0x0a0a1a, 5, 20)

  // Camera
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100)
  camera.position.set(5, 3, 5)
  camera.lookAt(0, 1, 0)

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  container.value.appendChild(renderer.domElement)

  // Lights
  const ambientLight = new THREE.AmbientLight(0x8B5CF6, 0.3)
  scene.add(ambientLight)

  const dirLight = new THREE.DirectionalLight(0x22D3EE, 0.8)
  dirLight.position.set(5, 10, 5)
  dirLight.castShadow = true
  scene.add(dirLight)

  const purpleLight = new THREE.PointLight(0xEC4899, 0.5, 10)
  purpleLight.position.set(-2, 3, -2)
  scene.add(purpleLight)

  // Greenhouse structure - 玻璃温室效果
  const greenhouseGroup = new THREE.Group()
  
  // 主结构框架 - 半透明玻璃效果
  const frameGeometry = new THREE.BoxGeometry(4, 3, 4)
  const frameMaterial = new THREE.MeshBasicMaterial({
    color: 0x22D3EE,
    transparent: true,
    opacity: 0.1,
    side: THREE.DoubleSide
  })
  const frame = new THREE.Mesh(frameGeometry, frameMaterial)
  frame.position.y = 1.5
  greenhouseGroup.add(frame)
  
  // 边框线条
  const edges = new THREE.EdgesGeometry(frameGeometry)
  const lineMaterial = new THREE.LineBasicMaterial({ color: 0x22D3EE, transparent: true, opacity: 0.5 })
  const wireframe = new THREE.LineSegments(edges, lineMaterial)
  wireframe.position.y = 1.5
  greenhouseGroup.add(wireframe)
  
  // 顶部装饰灯带
  const lightStripGeometry = new THREE.BoxGeometry(3.8, 0.05, 3.8)
  const lightStripMaterial = new THREE.MeshBasicMaterial({ 
    color: 0x8B5CF6, 
    transparent: true, 
    opacity: 0.3 
  })
  const lightStrip = new THREE.Mesh(lightStripGeometry, lightStripMaterial)
  lightStrip.position.y = 2.9
  greenhouseGroup.add(lightStrip)

  // Floor
  const floorGeometry = new THREE.PlaneGeometry(4, 4)
  const floorMaterial = new THREE.MeshLambertMaterial({ 
    color: 0x1a1a2e,
    side: THREE.DoubleSide
  })
  const floor = new THREE.Mesh(floorGeometry, floorMaterial)
  floor.rotation.x = -Math.PI / 2
  floor.receiveShadow = true
  greenhouseGroup.add(floor)

  scene.add(greenhouseGroup)
  greenhouse = greenhouseGroup

  // Plant representation based on growth stage
  createPlant()

  // Animation
  animate()
  loading.value = false
}

const createPlant = () => {
  if (plant) scene.remove(plant)
  
  plant = new THREE.Group()
  
  // Growth factor based on progress
  const growth = 0.3 + props.dayProgress * 0.7
  
  // Pot
  const potGeometry = new THREE.CylinderGeometry(0.3 * growth, 0.2 * growth, 0.4, 8)
  const potMaterial = new THREE.MeshLambertMaterial({ color: 0x8B4513 })
  const pot = new THREE.Mesh(potGeometry, potMaterial)
  pot.position.y = 0.2
  pot.castShadow = true
  plant.add(pot)
  
  // Soil
  const soilGeometry = new THREE.CircleGeometry(0.25 * growth, 8)
  const soilMaterial = new THREE.MeshLambertMaterial({ color: 0x3d2817 })
  const soil = new THREE.Mesh(soilGeometry, soilMaterial)
  soil.rotation.x = -Math.PI / 2
  soil.position.y = 0.38
  plant.add(soil)

  // Main stem
  const stemHeight = 0.5 * growth
  const stemGeometry = new THREE.CylinderGeometry(0.02 * growth, 0.03 * growth, stemHeight, 6)
  const stemMaterial = new THREE.MeshLambertMaterial({ color: 0x228B22 })
  const stem = new THREE.Mesh(stemGeometry, stemMaterial)
  stem.position.y = 0.4 + stemHeight / 2
  stem.castShadow = true
  plant.add(stem)

  // Leaves based on stage
  const leafCount = props.stageName === '萌芽' ? 2 : props.stageName === '生长期' ? 4 : 6
  const leafColor = props.stageName === '膨大' ? 0xFF69B4 : 0x32CD32
  
  for (let i = 0; i < leafCount; i++) {
    const angle = (i / leafCount) * Math.PI * 2
    const leafSize = 0.15 * growth * (props.stageName === '膨大' ? 1.5 : 1)
    
    const leafGeometry = new THREE.SphereGeometry(leafSize, 6, 4)
    leafGeometry.scale(1, 0.3, 0.5)
    const leafMaterial = new THREE.MeshLambertMaterial({ 
      color: leafColor,
      emissive: props.stageName === '膨大' ? 0xFF1493 : 0x000000,
      emissiveIntensity: props.stageName === '膨大' ? 0.2 : 0
    })
    const leaf = new THREE.Mesh(leafGeometry, leafMaterial)
    
    const height = 0.4 + (stemHeight * 0.3) + (i * 0.1 * growth)
    leaf.position.set(
      Math.cos(angle) * 0.15 * growth,
      height,
      Math.sin(angle) * 0.15 * growth
    )
    leaf.rotation.y = angle
    leaf.rotation.z = Math.PI / 6
    leaf.castShadow = true
    plant.add(leaf)
  }

  // Flower/Bud for later stages
  if (props.stageName === '分化' || props.stageName === '膨大') {
    const flowerGeometry = new THREE.SphereGeometry(0.1 * growth, 8, 6)
    const flowerMaterial = new THREE.MeshLambertMaterial({ 
      color: props.stageName === '膨大' ? 0xFF1493 : 0xFFB6C1,
      emissive: 0xFF1493,
      emissiveIntensity: 0.3
    })
    const flower = new THREE.Mesh(flowerGeometry, flowerMaterial)
    flower.position.y = 0.4 + stemHeight + 0.1 * growth
    flower.castShadow = true
    plant.add(flower)
  }

  // Sensor nodes (glowing dots)
 const sensorPositions = [
    { x: -1.5, y: 2, z: 0, label: '空气' },
    { x: 0, y: 0.5, z: 0, label: '土壤' },
    { x: 1.5, y: 2, z: 0, label: '光照' }
  ]
  
  sensorPositions.forEach(pos => {
    const sensorGeometry = new THREE.SphereGeometry(0.05, 8, 8)
    const sensorMaterial = new THREE.MeshBasicMaterial({
      color: 0x22D3EE,
      transparent: true,
      opacity: 0.8
    })
    const sensor = new THREE.Mesh(sensorGeometry, sensorMaterial)
    sensor.position.set(pos.x, pos.y, pos.z)
    
    // Glow effect
    const glowGeometry = new THREE.SphereGeometry(0.1, 8, 8)
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: 0x22D3EE,
      transparent: true,
      opacity: 0.3
    })
    const glow = new THREE.Mesh(glowGeometry, glowMaterial)
    sensor.add(glow)
    
    plant.add(sensor)
  })

  scene.add(plant)
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  if (greenhouse) {
    greenhouse.rotation.y += rotateSpeed
  }
  if (plant) {
    plant.rotation.y += rotateSpeed
    // Gentle sway animation
    plant.rotation.z = Math.sin(Date.now() * 0.001) * 0.02
  }
  
  renderer.render(scene, camera)
}

const resetCamera = () => {
  if (camera) {
    camera.position.set(5, 3, 5)
    camera.lookAt(0, 1, 0)
  }
}

const handleResize = () => {
  if (!container.value || !camera || !renderer) return
  
  const width = container.value.clientWidth
  const height = container.value.clientHeight || 200
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

onMounted(() => {
  setTimeout(init, 100)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
  if (renderer) {
    renderer.dispose()
    if (container.value && renderer.domElement) {
      container.value.removeChild(renderer.domElement)
    }
  }
})

watch(() => props.stageName, () => {
  createPlant()
})

watch(() => props.dayProgress, () => {
  createPlant()
})
</script>
