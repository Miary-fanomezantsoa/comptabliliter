<template>
  <div class="gemini-chat">
    <h2>Chat avec Gemini</h2>

    <div class="chat-window">
      <div v-for="(msg, index) in messages" :key="index" :class="msg.sender">
        <strong>{{ msg.sender }}:</strong> {{ msg.text }}
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="chat-form">
      <input v-model="input" type="text" placeholder="Écris ton message..." />
      <button type="submit">Envoyer</button>
    </form>
  </div>
</template>

<script>
import { askGemini } from "../axios"; // ton fichier api modifié

export default {
  data() {
    return {
      input: "",
      messages: [], // { sender: "Vous" | "Gemini", text: "..."}
    };
  },
  methods: {
    async sendMessage() {
      if (!this.input) return;

      // Ajouter le message de l'utilisateur
      this.messages.push({ sender: "Vous", text: this.input });

      // Appel à Gemini
      const response = await askGemini(this.input);

      // Ajouter la réponse de Gemini
      this.messages.push({ sender: "Gemini", text: response });

      // Réinitialiser l'input
      this.input = "";
    },
  },
};
</script>

<style scoped>
.gemini-chat {
  max-width: 500px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

.chat-window {
  border: 1px solid #ccc;
  padding: 10px;
  height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.Vous {
  text-align: right;
  color: blue;
}

.Gemini {
  text-align: left;
  color: green;
}

.chat-form {
  display: flex;
}

.chat-form input {
  flex: 1;
  padding: 5px;
}

.chat-form button {
  padding: 5px 10px;
}
</style>
