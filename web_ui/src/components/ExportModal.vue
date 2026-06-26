<template>
  <a-modal v-model:visible="visible" title="导出设置" @ok="handleOk" @cancel="handleCancel">
    <a-form :model="form">
      <a-form-item label="导出范围" field="scope">
        <a-select v-model="form.scope" placeholder="请选择导出范围" disabled>
          <a-option value="all">指定页数</a-option>
          <a-option value="selected">已选文章</a-option>
        </a-select>
      </a-form-item>
      <a-form-item label="导出格式" field="format">
        <a-select v-model="form.format" placeholder="请选择导出格式" multiple>
          <a-option value="csv">Excel列表</a-option>
          <a-option value="md">MarkDown</a-option>
          <a-option value="json">JSON附加信息</a-option>
          <a-option value="pdf">PDF归档</a-option>
          <a-option value="docx">WORD文档</a-option>
        </a-select>
      </a-form-item>
      <a-form-item label="导出页数" field="limit" v-if="form.scope === 'all' || form.scope === 'current'">
        <a-input-number v-model="form.page_count" :min="1" :max="10000" />
      </a-form-item>
      <a-form-item label="文件名" field="zip_filename">
        <a-input v-model="form.zip_filename" placeholder="请输入导出文件名（可选）" />
      </a-form-item>
      <a-form-item label="保存位置" field="export_dir">
        <a-space direction="vertical" fill style="width: 100%;">
          <a-radio-group v-model="form.use_custom_dir">
            <a-radio :value="false">默认目录（可在「导出记录」下载）</a-radio>
            <a-radio :value="true">自选文件夹</a-radio>
          </a-radio-group>
          <template v-if="form.use_custom_dir">
            <a-input
              v-model="form.export_dir"
              :readonly="isDesktop"
              :placeholder="isDesktop ? '请选择保存文件夹' : '请输入服务器上的绝对路径'"
            />
            <a-space v-if="isDesktop">
              <a-button type="outline" @click="handlePickDirectory">
                选择文件夹
              </a-button>
              <a-button
                v-if="form.export_dir"
                type="text"
                @click="handleOpenDirectory"
              >
                在 Finder 中打开
              </a-button>
            </a-space>
          </template>
          <a-typography-text v-else type="secondary">
            {{ defaultExportDirHint }}
          </a-typography-text>
        </a-space>
      </a-form-item>
      <a-form-item label="导出选项" field="options">
        <a-space direction="vertical">
          <a-checkbox v-model="form.add_title">添加标题</a-checkbox>
          <a-checkbox v-model="form.remove_images">移除图片</a-checkbox>
          <a-checkbox v-model="form.remove_links">移除链接</a-checkbox>
        </a-space>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Message } from '@arco-design/web-vue'
import { exportArticles, getExportLastResult } from '@/api/tools'
import { isDesktopApp } from '@/utils/auth'
import {
  getDefaultExportDirectory,
  openExportDirectory,
  pickExportDirectory
} from '@/utils/exportDir'

const buildExportTimestamp = () => {
  const now = new Date()
  const pad = (value: number) => String(value).padStart(2, '0')
  return `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`
}

const buildDefaultZipFilename = (mpName?: string) => {
  const timestamp = buildExportTimestamp()
  if (mpName && mpName !== '全部') {
    return `${mpName}_文章_${timestamp}.zip`
  }
  return `全部文章_${timestamp}.zip`
}

const DEFAULT_EXPORT_FORMAT = ['json', 'md']

const createDefaultForm = (mpName?: string) => ({
  scope: 'all',
  format: [...DEFAULT_EXPORT_FORMAT],
  page_count: 10,
  mp_id: '',
  ids: [] as string[],
  add_title: true,
  remove_images: false,
  remove_links: false,
  zip_filename: buildDefaultZipFilename(mpName),
  use_custom_dir: false,
  export_dir: ''
})

const visible = ref(false)
const isDesktop = computed(() => isDesktopApp())
const defaultExportDir = ref('')
const form = ref(createDefaultForm())

const defaultExportDirHint = computed(() => {
  if (defaultExportDir.value) {
    return `默认保存到：${defaultExportDir.value}`
  }
  return '默认保存到应用数据目录下的 data/docs/'
})

const emit = defineEmits(['confirm'])

const loadDefaultExportDir = async () => {
  if (!isDesktopApp()) {
    defaultExportDir.value = ''
    return
  }
  defaultExportDir.value = (await getDefaultExportDirectory()) || ''
}

const show = async (mp_id: string, ids: string[], mp_name?: string) => {
  const defaults = createDefaultForm(mp_name)
  form.value = {
    ...defaults,
    mp_id: mp_id || '',
    scope: ids && ids.length > 0 ? 'selected' : 'all',
    ids: ids || []
  }

  visible.value = true

  await loadDefaultExportDir()
  if (form.value.use_custom_dir && defaultExportDir.value) {
    form.value.export_dir = defaultExportDir.value
  }
}

const hide = () => {
  visible.value = false
}

const handlePickDirectory = async () => {
  const selected = await pickExportDirectory(form.value.export_dir || defaultExportDir.value)
  if (selected) {
    form.value.export_dir = selected
    form.value.use_custom_dir = true
  }
}

const handleOpenDirectory = async () => {
  if (!form.value.export_dir) {
    return
  }
  const opened = await openExportDirectory(form.value.export_dir)
  if (!opened) {
    Message.warning('无法打开该目录')
  }
}

const handleOk = async () => {
  if (form.value.use_custom_dir) {
    if (!form.value.export_dir) {
      Message.warning('请先选择保存文件夹')
      return
    }
  }
  await submitExport(form.value)
  emit('confirm', form.value)
  hide()
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

const pollExportResult = async (startedAt: string, mpId: string) => {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    await sleep(3000)
    try {
      const response = await getExportLastResult({ mp_id: mpId })
      const result = response?.data ?? response
      if (!result || !result.updated_at || result.updated_at <= startedAt) {
        continue
      }
      if (result.status === 'running') {
        continue
      }
      if (result.status === 'failed') {
        Message.error(result.message || '导出失败')
        return
      }
      if (result.status === 'partial' || (result.summary?.pdf_failed_count ?? 0) > 0) {
        Message.warning(result.message || '部分文章 PDF 导出失败')
        return
      }
      Message.success(result.message || '导出完成')
      return
    } catch (error) {
      console.error('查询导出结果失败:', error)
    }
  }
  Message.info('导出仍在进行，请稍后在「导出记录」中查看')
}

const submitExport = async (params: typeof form.value) => {
  const startedAt = new Date().toISOString()
  try {
    const result = await exportArticles(params)
    const exportPath = result.export_path || result.export_dir
    if (result.custom_dir && exportPath) {
      Message.success(`${result.message}\n${exportPath}`)
    } else {
      Message.success(result.message || '导出任务已启动')
    }
    void pollExportResult(startedAt, params.mp_id || '')
  } catch (error) {
    console.error('导出失败:', error)
  }
}

const handleCancel = () => {
  hide()
}

defineExpose({
  show,
  hide
})
</script>
