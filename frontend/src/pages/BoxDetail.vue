<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const props = defineProps({ id: String })
const box = ref(null)
const est = ref(null)
const bleedMm = ref(0)
const err = ref('')
const estErr = ref('')

async function applyBleed() {
  estErr.value = ''
  const bleed = bleedMm.value === '' || bleedMm.value == null ? null : Number(bleedMm.value)
  try {
    est.value = await getJSON(`/api/estimate?box_id=${props.id}${bleed == null ? '' : `&bleed_mm=${bleed}`}`)
  } catch (e) {
    est.value = null
    estErr.value = String(e.message || e)
  }
}

onMounted(async () => {
  try {
    const [b, s] = await Promise.all([getJSON(`/api/boxes/${props.id}`), getJSON('/api/settings')])
    box.value = b
    bleedMm.value = Number(s.bleed_mm ?? 0)
    if (b.data_quality !== 'dirty') await applyBleed()
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="box">
      <h1>{{ box.name }}</h1>
      <p class="lede">
        {{ box.length }} × {{ box.width }} × {{ box.height }} m
        <span class="pill" :class="{ warn: box.data_quality === 'dirty' }">
          {{ box.data_quality === 'dirty' ? '脏数据' : '可用' }}
        </span>
      </p>
      <p v-if="box.data_quality === 'dirty'" class="bad">{{ box.note }}</p>
      <template v-else>
        <div class="row">
          <label class="field">
            出血(mm)
            <input v-model.number="bleedMm" type="number" min="0" step="0.5" />
          </label>
          <button class="ghost" @click="applyBleed">应用出血</button>
        </div>
        <p v-if="estErr" class="bad">{{ estErr }}</p>
        <p v-if="est" class="stat-line">
          出血 {{ est.bleed_mm }} mm · 加边后 {{ est.eff_length }} × {{ est.eff_width }} × {{ est.eff_height }} m
          · 估算用纸 <strong>{{ est.paper_m2 }}</strong> m²
        </p>
      </template>
      <BoxUnfold
        v-if="est"
        :l="est.eff_length"
        :w="est.eff_width"
        :h="est.eff_height"
        :bleed-mm="est.bleed_mm"
      />
      <BoxUnfold v-else :l="box.length" :w="box.width" :h="box.height" />
      <div class="row" style="margin-top: 1.25rem">
        <router-link class="btn" to="/bench">用此盒去算纸</router-link>
        <router-link class="btn ghost" to="/boxes">返回清单</router-link>
      </div>
    </template>
  </div>
</template>
