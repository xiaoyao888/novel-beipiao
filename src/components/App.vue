<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElContainer, ElAside, ElMain, ElMenu, ElMenuItem, ElSubMenu, ElCard, ElButton, ElBacktop, ElMessage } from 'element-plus'
import { Reading, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { chapters } from '../data/chapters';

const currentIndex = ref(0)
const currentChapter = computed(() => chapters[currentIndex.value])
const chapterContent = ref('')
const loading = ref(false)
const chapterTitles = ref(chapters.map(c => c.title))

const menuItems = computed(() => {
  const volumes = [
    { id: 'volume1', name: '第一卷：离乡', chapters: chapters.filter(c => c.volume === '第一卷：离乡') },
    { id: 'volume2', name: '第二卷', chapters: chapters.filter(c => c.volume === '第二卷') },
    { id: 'volume3', name: '第三部：而立之年', chapters: chapters.filter(c => c.volume === '第三部：而立之年') }
  ];
  
  return volumes.map(volume => ({
    title: volume.name,
    chapters: volume.chapters
  }))
})

const getChapterTitle = (index) => {
  return chapterTitles.value[index] || chapters[index]?.title || ''
}

const extractTitleFromMarkdown = (text) => {
  const h2Match = text.match(/^##\s+(.+)$/m)
  if (h2Match) {
    const rawTitle = h2Match[1]
    const cleaned = rawTitle.replace(/[�?]/g, '').trim()
    return cleaned || null
  }
  return null
}

const loadChapterTitles = async () => {
  for (let i = 0; i < chapters.length; i++) {
    try {
      const response = await fetch(`/chapters/${chapters[i].id}.md`)
      const text = await response.text()
      const extractedTitle = extractTitleFromMarkdown(text)
      if (extractedTitle && extractedTitle !== '') {
        chapterTitles.value[i] = chapters[i].title.replace(/第\d+章\s*/, '') + extractedTitle
      }
    } catch (error) {
      console.log(`Failed to load title for chapter ${i}`)
    }
  }
}

const loadChapter = async (index) => {
  if (index < 0 || index >= chapters.length) return
  
  currentIndex.value = index
  loading.value = true
  
  try {
    const response = await fetch(`/chapters/${chapters[index].id}.md`)
    const text = await response.text()
    chapterContent.value = markdownToHtml(text)
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
  const chapterIndex = parseInt(index)
  loadChapter(chapterIndex)
}

onMounted(() => {
  loadChapterTitles()
  loadChapter(0)
})
</script>

<template>
  <el-container class="app-container">
    <el-aside width="300px" class="sidebar">
      <div class="logo">
        <el-icon :size="24"><Reading /></el-icon>
        <span>北漂</span>
      </div>
      
      <el-menu
        :default-active="currentIndex.toString()"
        class="chapter-menu"
        @select="handleMenuSelect"
      >
        <el-sub-menu
          v-for="(volume, vIndex) in menuItems"
          :key="vIndex"
          :index="vIndex.toString()"
        >
          <template #title>
            <span>{{ volume.title }}</span>
          </template>
          <el-menu-item
            v-for="chapter in volume.chapters"
            :key="chapter.globalIndex"
            :index="chapter.globalIndex.toString()"
          >
            {{ getChapterTitle(chapter.globalIndex) }}
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    
    <el-main class="content-area">
      <el-card class="chapter-card" v-loading="loading">
        <template #header>
          <div class="card-header">
            <div class="volume-tag">{{ currentChapter.volume }}</div>
            <h1 class="chapter-title">{{ getChapterTitle(currentIndex) }}</h1>
          </div>
        </template>
        
        <div class="chapter-content" v-html="chapterContent"></div>
        
        <div class="nav-buttons">
          <el-button 
            type="primary" 
            :icon="ArrowLeft" 
            @click="prevChapter"
            :disabled="currentIndex === 0"
          >
            上一章
          </el-button>
          <el-button 
            type="primary" 
            :icon="ArrowRight" 
            @click="nextChapter"
            :disabled="currentIndex === chapters.length - 1"
          >
            下一章
          </el-button>
        </div>
      </el-card>
      
      <div class="footer">© 2024 北漂 - 一个关于奋斗与成长的故事</div>
      
      <el-backtop :right="40" :bottom="40" />
    </el-main>
  </el-container>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
}

.sidebar {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #eee;
}

.chapter-menu {
  border-right: none;
}

.content-area {
  padding: 40px;
  overflow-y: auto;
}

.chapter-card {
  min-height: 600px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
}

.volume-tag {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  margin-bottom: 15px;
}

.chapter-title {
  font-size: 32px;
  color: #333;
  margin: 0;
}

.chapter-content {
  line-height: 2;
  color: #444;
  font-size: 16px;
  padding: 20px 0;
}

.chapter-content p {
  margin-bottom: 20px;
  text-indent: 2em;
}

.chapter-content h2 {
  font-size: 22px;
  color: #333;
  margin: 30px 0 15px;
  padding-left: 10px;
  border-left: 4px solid #667eea;
}

.chapter-content hr {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, #ddd, transparent);
  margin: 40px 0;
}

.chapter-content em {
  color: #888;
  font-style: normal;
}

.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.footer {
  text-align: center;
  padding: 20px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100% !important;
    max-height: 300px;
  }
  
  .content-area {
    padding: 20px;
  }
  
  .chapter-title {
    font-size: 24px;
  }
}
</style>