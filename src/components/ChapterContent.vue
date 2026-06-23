<script setup>
import { ref } from 'vue'
import { ElCard, ElButton, ElBacktop, ElMessage } from 'element-plus'
import { ArrowLeft, ArrowRight, CopyDocument } from '@element-plus/icons-vue'

const props = defineProps({
  volume: {
    type: String,
    default: ''
  },
  chapterTitle: {
    type: String,
    default: ''
  },
  chapterContent: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  currentIndex: {
    type: Number,
    default: 0
  },
  totalChapters: {
    type: Number,
    default: 0
  },
  darkMode: {
    type: Boolean,
    default: false
  },

})

const emit = defineEmits(['prev', 'next'])
const copied = ref(false)

const prevChapter = () => {
  emit('prev')
}

const nextChapter = () => {
  emit('next')
}

const copyContent = async () => {
  try {
    const text = props.chapterContent.replace(/<[^>]*>/g, '').replace(/\n+/g, '\n').trim()
    await navigator.clipboard.writeText(text)
    copied.value = true
    ElMessage.success('复制成功')
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    ElMessage.error('复制失败')
  }
}
</script>

<template>
  <el-card :class="['chapter-card', { 'dark': darkMode }]" v-loading="loading">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <div class="volume-tag">{{ volume }}</div>
          <h1 class="chapter-title">{{ chapterTitle }}</h1>
        </div>
        <el-button 
          :icon="CopyDocument" 
          @click="copyContent"
          :type="copied ? 'success' : 'default'"
          size="small"
        >
          {{ copied ? '已复制' : '复制' }}
        </el-button>
      </div>
    </template>
    
    <div class="chapter-content" :class="{'dark': darkMode}"  v-html="chapterContent"></div>
    
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
        :disabled="currentIndex === totalChapters - 1"
      >
        下一章
      </el-button>
    </div>
  </el-card>
  
  <div class="footer">© 2024 北漂 - 一个关于奋斗与成长的故事</div>
  
  <el-backtop :right="40" :bottom="40" />
</template>

<style scoped>
.chapter-card {
  min-height: 600px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: transparent;

}
.chapter-card.dark {
  background: #1e1e32f2;
}



.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
  text-align: center;
}

.volume-tag {
  display: inline-block;
  padding: 4px 12px;
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
.chapter-content.dark{
  color:#adabab;
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
  .chapter-title {
    font-size: 24px;
  }
}
</style>
