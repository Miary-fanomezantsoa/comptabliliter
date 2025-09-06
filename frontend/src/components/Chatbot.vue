<template>
  <div class="flex flex-col h-[80vh] max-h-[80vh] bg-amber-100 rounded-xl shadow-lg mx-auto my-6 w-full md:w-3/4 lg:w-1/2">
    <!-- Header -->
    <header class="bg-amber-700 text-white p-4 flex items-center justify-between rounded-t-xl shadow-md">
      <div class="flex items-center gap-2">
        <MessageCircle class="w-6 h-6" />
        <span class="font-bold text-xl">Chatbot</span>
      </div>
    </header>

    <!-- Messages -->
    <main v-if="isOpen" ref="chatBox" class="flex-1 overflow-y-auto p-6 space-y-4 bg-amber-50">
      <div v-for="(msg, index) in messages" :key="index" class="flex" :class="msg.user === 'me' ? 'justify-end' : 'justify-start'">
        <div :class="[
              'inline-block p-4 rounded-2xl max-w-[70%] break-words',
              msg.user === 'me' ? 'bg-amber-700 text-white rounded-br-none' : 'bg-amber-200 text-amber-900 rounded-bl-none'
            ]">
          {{ msg.text }}
        </div>
      </div>
    </main>

    <!-- Input -->
    <form v-if="isOpen" @submit.prevent="sendMessage" class="flex p-4 border-t bg-amber-100 shadow-inner gap-3 rounded-b-xl">
      <input
        v-model="input"
        type="text"
        placeholder="Écris un message..."
        class="flex-1 p-3 border border-amber-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-amber-500 bg-amber-50"
      />
      <button type="submit" class="bg-amber-700 text-white px-4 py-2 rounded-2xl flex items-center gap-2 hover:bg-amber-800 transition-colors">
        <Send class="w-5 h-5" /> Envoyer
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import api from '../axios'
import { MessageCircle, Send, X } from 'lucide-vue-next'

const messages = ref([])
const input = ref("")
const chatBox = ref(null)
const isOpen = ref(true)

const sendMessage = async () => {
  if (!input.value.trim()) return

  messages.value.push({ user: "me", text: input.value })
  const userInput = input.value
  input.value = ""

  await nextTick()
  chatBox.value.scrollTop = chatBox.value.scrollHeight

  try {
    const res = await api.post("/ai/chat/", { message: userInput })
    messages.value.push({ user: "bot", text: res.data.reply })

    await nextTick()
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  } catch (err) {
    console.error("Erreur API chatbot:", err)
    messages.value.push({ user: "bot", text: "Le bot est indisponible." })
  }
}
</script>
