document.addEventListener('DOMContentLoaded', () => {

    const openAiButton = document.getElementById('open-ai-btn');
    const aiChatContainer = document.getElementById('ai-chat-container');
    const closeAiButton = document.getElementById('close-ai-btn');
    const submitPromptButton = document.getElementById('submit-ai-prompt');
    const promptInput = document.getElementById('ai-prompt-input');

    openAiButton.addEventListener('click', () => {
        aiChatContainer.classList.remove('hidden');
    });

    closeAiButton.addEventListener('click', () => {
        aiChatContainer.classList.add('hidden');
    });

    submitPromptButton.addEventListener('click', () => {
        const promptText = promptInput.value;

        if (promptText.trim() === ''){
            alert('Por favor, digite algo para a IA.');
            return;
        }

        alert('Prompt enviado para a IA:\n"${promptText}"');

        promptInput.value = '';
        aiChatContainer.classList.add('hidden');
    });
});