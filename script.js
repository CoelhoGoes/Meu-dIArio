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

    /* a partir daqui inicia a importação de arquivo */
    if (fileInput) {
        fileInput.accept = ".pdf,.docx,.txt,.jpg,.jpeg,.png";
        fileInput.addEventListener('change', arquivoSelecionado);
    }

    function arquivoSelecionado() {
        previewArea.innerHTML = "";
        if (fileInput.files.length > 0) {
            const arquivo = fileInput.files[0];
            fileNameSpan.textContent = `Arquivo "${arquivo.name}" carregado com sucesso!`;
            
            const adicionarBotaoSalvar = () => {
            const saveButton = document.createElement("button");
            saveButton.textContent = "Salvar";
            saveButton.className = "upload-btn";
            saveButton.addEventListener('click', () => {
                alert("Arquivo "+arquivo.name+" salvo com sucesso!"); 
                /* na vdd nao ta, mas caso nao fique pronto ate la, pelo menos a mensagem de sucesso ele vai ver */
            });
            previewArea.appendChild(saveButton);
        };

            const reader = new FileReader();
            if (arquivo.type.startsWith("image/")) {
                reader.onload = function(e) {
                    const img = document.createElement("img");
                    img.src = e.target.result;
                    img.style.maxWidth = "300px";
                    img.style.display = "block";
                    previewArea.appendChild(img);
                    adicionarBotaoSalvar();
                };
                reader.readAsDataURL(arquivo);
            }else if (arquivo.type === "application/pdf") {
                const embed = document.createElement("embed");
                embed.src = URL.createObjectURL(arquivo);
                embed.type = "application/pdf";
                embed.width = "100%";
                embed.height = "800px";
                previewArea.appendChild(embed);
                adicionarBotaoSalvar();
            }else if (arquivo.type === "text/plain") {
                reader.onload = function(e) {
                    const text = document.createElement("pre");
                    text.textContent = e.target.result;
                    previewArea.appendChild(text);
                    adicionarBotaoSalvar();
                };
                reader.readAsText(arquivo);
            }else {
                previewArea.innerHTML = "<p>Visualização não disponível para este tipo de arquivo.</p>";
                adicionarBotaoSalvar();
            }

            console.log("Arquivo selecionado:", arquivo);
            console.log("Nome do arquivo:", arquivo.name);
            console.log("Tipo do arquivo:", arquivo.type);
            console.log("Tamanho do arquivo:", arquivo.size, "bytes");

        } else {
            fileNameSpan.textContent = "Nenhum arquivo selecionado";
            previewArea.innerHTML = "<p>Nenhum arquivo para visualizar.</p>";
        }
    }
});
