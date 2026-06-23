<script setup>
import { ElMenu, ElMenuItem, ElSubMenu } from 'element-plus'

defineProps({
  menuItems: {
    type: Array,
    required: true
  },
  currentIndex: {
    type: Number,
    default: 0
  },
  chapterTitles: {
    type: Array,
    default: () => []
  },
  chapters: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['select'])

const getChapterTitle = (index, chapterTitles, chapters) => {
  return chapterTitles[index] || chapters[index]?.title || ''
}

const handleMenuSelect = (index) => {
  emit('select', parseInt(index))
}
</script>

<template>
  <div class="logo">
    <span>北漂十七年</span>
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
        {{ getChapterTitle(chapter.globalIndex, chapterTitles, chapters) }}
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #eee;
  justify-content: center;
  transition: color 0.3s ease;
}

.dark .logo {
  color: #fff;
  border-bottom-color: #333;
}

.chapter-menu {
  border-right: none;
}

.dark .chapter-menu {
  color: #a0aec0;
}

.dark .el-menu-item {
  color: #a0aec0;
}

.dark .el-menu-item:hover,
.dark .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.dark .el-submenu__title {
  color: #a0aec0;
}

.dark .el-submenu__title:hover {
  color: #fff;
}
</style>
