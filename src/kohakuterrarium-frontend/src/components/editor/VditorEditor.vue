<template>
  <div ref="editorEl" class="h-full w-full" />
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import Vditor from "vditor";
import "vditor/dist/index.css";

const props = defineProps({
  content: { type: String, default: "" },
  filePath: { type: String, default: "" },
});

const emit = defineEmits(["change", "save"]);

const editorEl = ref(null);
let vd = null;
let suppressChange = false;

onMounted(() => {
  if (!editorEl.value) return;

  vd = new Vditor(editorEl.value, {
    mode: "ir", // instant rendering (WYSIWYG-ish)
    value: props.content,
    height: "100%",
    toolbarConfig: { pin: true },
    toolbar: [
      "headings", "bold", "italic", "strike", "|",
      "list", "ordered-list", "check", "|",
      "quote", "code", "inline-code", "|",
      "link", "table", "|",
      "undo", "redo", "|",
      "edit-mode", "outline", "fullscreen",
    ],
    cache: { enable: false },
    theme: document.documentElement.classList.contains("dark") ? "dark" : "classic",
    preview: {
      theme: { current: document.documentElement.classList.contains("dark") ? "dark" : "light" },
      hljs: { lineNumber: true },
      math: { engine: "KaTeX" },
    },
    input: (value) => {
      if (!suppressChange) {
        emit("change", value);
      }
    },
    ctrlEnter: () => {
      emit("save");
    },
    after: () => {
      // Focus the editor after init.
      vd?.focus();
    },
  });
});

// Sync external content changes (e.g. file revert).
watch(
  () => props.content,
  (newVal) => {
    if (!vd) return;
    const current = vd.getValue();
    if (current !== newVal) {
      suppressChange = true;
      vd.setValue(newVal);
      suppressChange = false;
    }
  },
);

// Watch dark mode changes.
watch(
  () => document.documentElement.classList.contains("dark"),
  (dark) => {
    if (vd) {
      vd.setTheme(dark ? "dark" : "classic");
    }
  },
);

onUnmounted(() => {
  if (vd) {
    vd.destroy();
    vd = null;
  }
});
</script>

<style>
/* Override vditor to fill container */
.vditor {
  border: none !important;
  border-radius: 0 !important;
}
</style>
