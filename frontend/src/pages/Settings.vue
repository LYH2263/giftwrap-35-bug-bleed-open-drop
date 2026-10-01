<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'

const s = ref({})
const bleed = ref('0')
const err = ref('')
const saved = ref(false)

onMounted(async () => {
  try {
    s.value = await getJSON('/api/settings')
    bleed.value = String(s.value.bleed_mm ?? '0')
  } catch (e) {
    err.value = String(e.message || e)
  }
})

async function saveBleed() {
  err.value = ''
  saved.value = false
  try {
    s.value = await putJSON('/api/settings', { bleed_mm: Number(bleed.value) })
    bleed.value = String(s.value.bleed_mm)
    saved.value = true
  } catch (e) {
    err.value = String(e.message || e)
  }
}
</script>

<template>
  <div class="page">
    <h1>设置</h1>
    <p class="lede">默认出血只影响新测算；已写入用纸档的记录按写入值钉住，不回溯重算。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <ul class="item-list">
      <li>
        <span>折边系数 overlap</span>
        <span class="meta">{{ s.overlap }}</span>
      </li>
      <li>
        <span>默认出血 bleed_mm</span>
        <span class="meta">
          <label class="field">
            <input v-model="bleed" type="number" min="0" step="0.5" /> mm
          </label>
          <button :disabled="!s.overlap" @click="saveBleed">保存</button>
        </span>
      </li>
    </ul>
    <p v-if="saved" class="stat-line">已保存，新测算将按 {{ s.bleed_mm }} mm 出血试算。</p>
  </div>
</template>
