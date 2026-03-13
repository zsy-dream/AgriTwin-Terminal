import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    sidebarOpen: true,
    activeGreenhouseId: 1
  }),
  actions: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },
    setActiveGreenhouse(id) {
      this.activeGreenhouseId = id
    }
  }
})
