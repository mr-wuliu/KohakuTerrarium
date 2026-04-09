<template>
  <div
    class="preset-strip flex items-center gap-1 px-2 h-7 border-b border-warm-200 dark:border-warm-700 bg-warm-50 dark:bg-warm-900 text-[11px]"
  >
    <div class="i-carbon-layout text-sm text-warm-400 mr-1" />

    <button
      v-for="p in presets"
      :key="p.id"
      class="preset-chip flex items-center gap-1 px-2 py-0.5 rounded transition-colors"
      :class="active === p.id
        ? 'bg-iolite/15 text-iolite dark:text-iolite-light'
        : 'text-warm-500 hover:text-warm-700 dark:hover:text-warm-300 hover:bg-warm-100 dark:hover:bg-warm-800'"
      :title="p.shortcut ? `${p.label} (${p.shortcut})` : p.label"
      @click="onSelect(p.id)"
    >
      <span class="truncate max-w-24">{{ p.label }}</span>
      <span
        v-if="p.shortcut"
        class="text-[9px] opacity-60 font-mono"
      >{{ p.shortcut }}</span>
    </button>

    <div class="flex-1" />

    <!-- Save-as-new-preset stub. Phase 5 wires the modal. -->
    <button
      class="w-6 h-6 flex items-center justify-center rounded text-warm-400 hover:text-warm-600 dark:hover:text-warm-300 transition-colors"
      title="Save current as new preset (Phase 5)"
      @click="onSaveAs"
    >
      <div class="i-carbon-add text-sm" />
    </button>

    <!-- Edit-layout toggle stub. Phase 5 opens edit mode. -->
    <button
      class="w-6 h-6 flex items-center justify-center rounded text-warm-400 hover:text-warm-600 dark:hover:text-warm-300 transition-colors"
      title="Customize layout (Ctrl+Shift+L)"
      @click="onEdit"
    >
      <div class="i-carbon-edit text-sm" />
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue";

import { useLayoutStore } from "@/stores/layout";
import { fireLayoutEditRequested, fireLayoutSaveAsRequested } from "@/utils/layoutEvents";

const layout = useLayoutStore();

/** Order the strip in the canonical preset order. */
const PRESET_ORDER = [
  "chat-focus",
  "workspace",
  "multi-creature",
  "canvas",
  "debug",
  "settings",
];

const presets = computed(() => {
  const all = layout.allPresets;
  const out = [];
  for (const id of PRESET_ORDER) {
    if (all[id]) out.push(all[id]);
  }
  // Include any remaining user presets after the ordered builtins.
  for (const preset of Object.values(all)) {
    if (!PRESET_ORDER.includes(preset.id) && !preset.id.startsWith("legacy-")) {
      out.push(preset);
    }
  }
  return out;
});

const active = computed(() => layout.activePresetId);

function onSelect(id) {
  layout.switchPreset(id);
}

function onEdit() {
  fireLayoutEditRequested();
}

function onSaveAs() {
  fireLayoutSaveAsRequested();
}
</script>
