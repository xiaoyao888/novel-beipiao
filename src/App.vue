<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElContainer, ElAside, ElMain, ElMessage } from 'element-plus'
import { chapters, volumes } from './beipiao/beipiao'
import SidebarMenu from './components/SidebarMenu.vue'
import ChapterContent from './components/ChapterContent.vue'

const currentIndex = ref(0)
const currentChapter = computed(() => chapters[currentIndex.value])
const chapterContent = ref('')
const loading = ref(false)

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
}

onMounted(() => {
  loadChapter(0)
})
</script>

<template>
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
        @prev="prevChapter"
        @next="nextChapter"
      />
    </el-main>
  </el-container>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
}

.sidebar {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
  max-height: 100vh;
  overflow-y: auto;
}

.content-area {
  padding: 40px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100% !important;
    max-height: 300px;
  }
  
  .content-area {
    padding: 20px;
  }
}
</style>
