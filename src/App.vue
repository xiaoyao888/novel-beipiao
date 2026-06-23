<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElContainer, ElAside, ElMain, ElMessage, ElDrawer, ElSwitch } from 'element-plus'
import { Menu, Moon } from '@element-plus/icons-vue'
import { chapters, volumes } from './beipiao/beipiao'
import SidebarMenu from './components/SidebarMenu.vue'
import ChapterContent from './components/ChapterContent.vue'

const currentIndex = ref(0)
const currentChapter = computed(() => chapters[currentIndex.value])
const chapterContent = ref('')
const loading = ref(false)
const drawerVisible = ref(false)
const darkMode = ref(false)

const chapterFiles = import.meta.glob('./beipiao/chapter-*.md', { as: 'raw' })

const menuItems = computed(() => {
  return volumes.map(volume => ({
    title: volume.name,
    chapters: chapters.filter(c => c.volume === volume.name)
  }))
})

const getChapterTitle = (index) => {
  return chapters[index]?.title || ''
}

const loadChapter = async (index) => {
  if (index < 0 || index >= chapters.length) return
  
  currentIndex.value = index
  loading.value = true
  
  try {
    const chapterId = chapters[index].id
    const filePath = `./beipiao/${chapterId}.md`
    const content = await chapterFiles[filePath]()
    chapterContent.value = markdownToHtml(content)
  } catch (error) {
    ElMessage.error('加载章节失败')
    chapterContent.value = '<p style="color: #999;">加载失败，请检查文件是否存在</p>'
  } finally {
    loading.value = false
  }
}

const markdownToHtml = (text) => {
  let processed = text.replace(/^#[^\n]+\n\n/, '')
  processed = processed.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>')
  processed = processed.replace(/^---+$/gm, '<hr>')
  processed = processed.replace(/^\*\((.+)\)$/gm, '<em>($1)</em>')
  
  const lines = processed.split(/\r?\n/)
  const htmlLines = lines.map(line => {
    const trimmed = line.trim()
    if (trimmed === '') return ''
    if (trimmed.startsWith('<h2>') || trimmed.startsWith('<hr>') || trimmed.startsWith('<em>')) {
      return trimmed
    }
    return '<p>' + trimmed + '</p>'
  })
  
  return htmlLines.join('\n')
}

const prevChapter = () => {
  if (currentIndex.value > 0) {
    loadChapter(currentIndex.value - 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const nextChapter = () => {
  if (currentIndex.value < chapters.length - 1) {
    loadChapter(currentIndex.value + 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handleMenuSelect = (index) => {
  loadChapter(index)
  drawerVisible.value = false
}

const openDrawer = () => {
  drawerVisible.value = true
}

const closeDrawer = () => {
  drawerVisible.value = false
}

onMounted(() => {
  loadChapter(0)
})
</script>

<template>
  <div :class="['app-wrapper', { 'dark': darkMode }]">
    <header class="top-header">
      <button class="header-menu-btn" @click="openDrawer">
        <Menu :size="20" />
      </button>
      <h1 class="header-title">北漂十七年</h1>
      <div class="header-right">
        <span class="dark-mode-label">{{ darkMode ? '暗夜模式' : '日间模式' }}</span>
        <ElSwitch 
          v-model="darkMode" 
          :active-icon="Moon" 
          :inactive-icon="Sun"
          active-color="#667eea"
          inactive-color="#ddd"
        />
      </div>
    </header>
    
    <el-container class="app-container">
      <el-aside width="300px" class="sidebar">
        <SidebarMenu
          :menu-items="menuItems"
          :current-index="currentIndex"
          :chapter-titles="chapters.map(c => c.title)"
          :chapters="chapters"
          @select="handleMenuSelect"
        />
      </el-aside>
      
      <el-main class="content-area">
        <ChapterContent
          :volume="currentChapter.volume"
          :chapter-title="getChapterTitle(currentIndex)"
          :chapter-content="chapterContent"
          :loading="loading"
          :current-index="currentIndex"
          :total-chapters="chapters.length"
          :dark-mode="darkMode"
          @prev="prevChapter"
          @next="nextChapter"
        />
      </el-main>
    </el-container>
    
    <el-drawer
      :visible="drawerVisible"
      :direction="'ltr'"
      :size="'80%'"
      class="mobile-drawer"
      @close="closeDrawer"
    >
      <div class="drawer-header">
        <span class="drawer-title">北漂十七年</span>
        <button class="close-btn" @click="closeDrawer">
          ×
        </button>
      </div>
      <SidebarMenu
        :menu-items="menuItems"
        :current-index="currentIndex"
        :chapter-titles="chapters.map(c => c.title)"
        :chapters="chapters"
        @select="handleMenuSelect"
      />
    </el-drawer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  min-height: 100vh;
  transition: background 0.3s ease;
  background: #f2f2f2;
}

.app-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f2f2f2 0%, #f5f5f5 100%);
}

.app-wrapper.dark {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.top-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: background 0.3s ease;
}

.app-wrapper.dark .top-header {
  background: rgba(30, 30, 50, 0.95);
}

.header-menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  transition: all 0.3s ease;
}

.app-wrapper.dark .header-menu-btn {
  color: #a0aec0;
}

.header-menu-btn:hover {
  background: rgba(102, 126, 234, 0.1);
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  transition: color 0.3s ease;
}

.app-wrapper.dark .header-title {
  color: #fff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dark-mode-label {
  font-size: 14px;
  color: #666;
  transition: color 0.3s ease;
}

.app-wrapper.dark .dark-mode-label {
  color: #a0aec0;
}

.app-container {
  min-height: 100vh;
  padding-top: 60px;
}

.sidebar {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
  max-height: calc(100vh - 60px);
  overflow-y: auto;
  transition: background 0.3s ease;
}

.app-wrapper.dark .sidebar {
  background: #303045f2;
}

.content-area {
  padding: 20px;
  overflow-y: auto;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 0;
}

.app-wrapper.dark .drawer-header {
  border-bottom-color: #333;
}

.drawer-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.app-wrapper.dark .drawer-title {
  color: #fff;
}

.close-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f5f5f5;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 24px;
  transition: all 0.3s ease;
}

.app-wrapper.dark .close-btn {
  background: #333;
  color: #a0aec0;
}

.close-btn:hover {
  background: #eee;
}

.app-wrapper.dark .close-btn:hover {
  background: #444;
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  
  .content-area {
    padding: 8px;
  }
  
  .header-menu-btn {
    display: flex;
  }
  
  .header-title {
    font-size: 16px;
  }
  
  .dark-mode-label {
    display: none;
  }
}

@media (min-width: 769px) {
  .header-menu-btn {
    display: none;
  }
}
</style>
