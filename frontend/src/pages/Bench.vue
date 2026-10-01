<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const route = useRoute()
const boxes = ref([])
const bid = ref(1)
const bleedMm = ref(0)
const out = ref(null)
const err = ref('')
const busy = ref(false)

onMounted(async () => {
  try {
    const [boxResp, settings] = await Promise.all([getJSON('/api/boxes'), getJSON('/api/settings')])
    boxes.value = boxResp.items.filter((b) => b.data_quality === 'clean')
    if (boxes.value.length) bid.value = boxes.value[0].id
    bleedMm.value = Number(settings.bleed_mm ?? 0)
    // 从用纸档详情「在算纸台复算」跳入时，带上当次盒与出血，便于与回看互证
    const qBox = Number(route.query.box_id)
    if (qBox && boxes.value.some((b) => b.id === qBox)) bid.value = qBox
    if (route.query.bleed_mm != null && route.query.bleed_mm !== '') {
      bleedMm.value = Number(route.query.bleed_mm)
    }
  } catch (e) {
    err.value = String(e.message || e)
  }
})

async function go(save) {
  err.value = ''
  busy.value = true
  // 输入框留空 → 不传 bleed_mm，走后端默认出血
  const bleed = bleedMm.value === '' || bleedMm.value == null ? null : Number(bleedMm.value)
  try {
    out.value = save
      ? await postJSON('/api/estimate', { box_id: bid.value, bleed_mm: bleed, save: true })
      : await getJSON(`/api/estimate?box_id=${bid.value}${bleed == null ? '' : `&bleed_mm=${bleed}`}`)
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>算纸</h1>
    <p class="lede">先试算看面积与展开，确认后再写入用纸档。出血按每边外扩计入有效几何。</p>
    <div class="row">
      <select v-model.number="bid">
        <option v-for="b in boxes" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <label class="field">
        出血(mm)
        <input v-model.number="bleedMm" type="number" min="0" step="0.5" />
      </label>
      <button :disabled="busy" @click="go(false)">试算</button>
      <button class="ribbon" :disabled="busy" @click="go(true)">写入用纸档</button>
    </div>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-if="out" class="result-board">
      <div class="figure">{{ out.paper_m2 }}<span>m²</span></div>
      <p class="stat-line">
        出血 {{ out.bleed_mm }} mm · 加边后 {{ out.eff_length }} × {{ out.eff_width }} × {{ out.eff_height }} m
      </p>
      <p class="stat-line" v-if="out.ribbon">
        十字丝带约 {{ out.ribbon.ribbon_m ?? out.ribbon }} m
      </p>
      <BoxUnfold
        :l="out.eff_length"
        :w="out.eff_width"
        :h="out.eff_height"
        :paper-m2="out.paper_m2"
        :bleed-mm="out.bleed_mm"
      />
    </div>
  </div>
</template>
