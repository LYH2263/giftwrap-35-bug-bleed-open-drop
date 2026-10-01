<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="run">
      <h1>用纸档 #{{ run.id }}</h1>
      <p class="lede">{{ run.box_name }} · 写入即钉住，改默认出血不回溯重算。</p>
      <div class="result-board">
        <div class="figure">{{ run.result.paper_m2 }}<span>m²</span></div>
        <p class="stat-line">
          出血 {{ run.result.bleed_mm ?? 0 }} mm · 折边系数 ×{{ run.overlap }} · 口径 {{ run.result.calc_order ?? '—' }}
        </p>
        <p v-if="run.result.eff_length != null" class="stat-line">
          加边后三边 {{ run.result.eff_length }} × {{ run.result.eff_width }} × {{ run.result.eff_height }} m
        </p>
        <p v-if="run.result.zero_bleed_paper_m2 != null" class="stat-line">
          零出血对照 {{ run.result.zero_bleed_paper_m2 }} m²（仅对照，非用纸面积）
        </p>
        <p class="stat-line">写入时间 {{ run.created_at }}</p>
        <BoxUnfold
          v-if="run.result.eff_length != null"
          :l="run.result.eff_length"
          :w="run.result.eff_width"
          :h="run.result.eff_height"
          :paper-m2="run.result.paper_m2"
          :bleed-mm="run.result.bleed_mm ?? 0"
        />
      </div>
      <div class="row" style="margin-top: 1.25rem">
        <router-link class="btn" :to="`/bench?box_id=${run.box_id}&bleed_mm=${run.result.bleed_mm ?? 0}`">
          在算纸台复算
        </router-link>
        <router-link class="btn ghost" to="/history">返回用纸档</router-link>
      </div>
    </template>
  </div>
</template>
