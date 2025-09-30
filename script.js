document.addEventListener('DOMContentLoaded', () => {

    const openAiPanelButton = document.getElementById('open-ai-panel-btn');
    const aiPanel = document.getElementById('ai-panel');
    const closeAiPanelButton = document.getElementById('close-ai-panel-btn');
    const submitPromptButton = document.getElementById('submit-ai-prompt');
    const promptInput = document.getElementById('ai-prompt-input');

    openAiPanelButton.addEventListener('click', () => {
        aiPanel.classList.remove('closed');
    });

    closeAiPanelButton.addEventListener('click', () => {
        aiPanel.classList.add('closed');
    });

    submitPromptButton.addEventListener('click', () => {
        const promptText = promptInput.value;

        if (promptText.trim() === ''){
            alert('Por favor, digite algo para a IA.');
            return;
        }

        alert('Prompt enviado para a IA:\n"${promptText}"');

        promptInput.value = '';
        aiPanel.classList.add('closed');
    });
});