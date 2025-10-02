document.addEventListener('DOMContentLoaded', () => {
    // --- SELETORES DE ELEMENTOS ---
    const loginOverlay = document.getElementById('login-overlay');
    const appContainer = document.getElementById('app-container');
    const loginBtn = document.getElementById('login-btn');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('login-error');

    const openAiPanelButton = document.getElementById('open-ai-panel-btn');
    const aiPanel = document.getElementById('ai-panel');
    const closeAiPanelButton = document.getElementById('close-ai-panel-btn');
    const submitPromptButton = document.getElementById('submit-ai-prompt');
    const promptInput = document.getElementById('ai-prompt-input');
    const responseContent = document.getElementById('ai-response-content');
    
    // --- ELEMENTOS PARA DIRETÓRIOS E ANOTAÇÕES ---
    const saveNoteBtn = document.getElementById('save-note-btn');
    const newNoteBtn = document.getElementById('new-note-btn');
    const mainEditor = document.getElementById('main-editor');
    const directoryList = document.getElementById('directory-list');
    const newDirectoryNameInput = document.getElementById('new-directory-name');
    const createDirectoryBtn = document.getElementById('create-directory-btn');

    // --- ESTRUTURA DE DADOS ---
    let directories = [{ id: Date.now(), name: 'Anotações Gerais', notes: [] }];
    let activeDirectoryId = directories[0].id;
    let activeNoteId = null;

    // --- ELEMENTOS DE UPLOAD ---
    const fileInput = document.getElementById("fileInput");
    const fileNameSpan = document.getElementById("fileName");
    const previewArea = document.getElementById("previewArea");

    // --- LÓGICA DE LOGIN ---
    loginBtn.addEventListener('click', () => {
        if (emailInput.value === 'teste@email.com' && passwordInput.value === '123') {
            loginOverlay.classList.add('hidden');
            appContainer.classList.remove('hidden');
            renderDirectoriesAndNotes(); // Renderiza o estado inicial ao logar
        } else {
            loginError.textContent = 'Email ou senha inválidos.';
        }
    });

    // --- LÓGICA DO PAINEL DA IA ---
    submitPromptButton.addEventListener('click', async () => {
        const promptText = promptInput.value;
        if (promptText.trim() === '') return alert('Por favor, digite algo para a IA.');
        
        // Pega o conteúdo da anotação atual como contexto
        const noteContext = mainEditor.value;

        submitPromptButton.disabled = true;
        submitPromptButton.textContent = 'Pensando...';
        responseContent.textContent = 'Aguarde...';
        try {
            const apiUrl = 'http://127.0.0.1:8000/ask-ia';
            // Codifica os parâmetros para a URL
            const encodedPrompt = encodeURIComponent(promptText);
            const encodedContext = encodeURIComponent(noteContext);
            const requestUrl = `${apiUrl}?prompt=${encodedPrompt}&contexto=${encodedContext}`;
            
            const response = await fetch(requestUrl);
            if (!response.ok) throw new Error(`Erro na API: ${response.status}`);
            const data = await response.json();
            responseContent.textContent = data.answer || 'Sem resposta válida.';
        } catch (error) {
            console.error('Falha ao buscar resposta da IA:', error);
            responseContent.textContent = 'Desculpe, não foi possível obter uma resposta.';
        } finally {
            submitPromptButton.disabled = false;
            submitPromptButton.textContent = 'Enviar para IA';
        }
    });

    // --- LÓGICA DE DIRETÓRIOS E ANOTAÇÕES ---

    createDirectoryBtn.addEventListener('click', () => {
        const newName = newDirectoryNameInput.value.trim();
        if (!newName) return alert('Por favor, insira um nome para a pasta.');

        const nameExists = directories.some(dir => dir.name.toLowerCase() === newName.toLowerCase());
        if (nameExists) {
            return alert('Erro: Já existe uma pasta com este nome.');
        }

        const newDirectory = { id: Date.now(), name: newName, notes: [] };
        directories.push(newDirectory);
        newDirectoryNameInput.value = '';
        renderDirectoriesAndNotes();
    });

    function saveOrUpdateCurrentNote() {
        const currentText = mainEditor.value.trim();
        if (!currentText) return false;

        const activeDir = directories.find(dir => dir.id === activeDirectoryId);
        if (!activeDir) return alert('Erro: Nenhuma pasta selecionada.');

        if (activeNoteId) {
            const note = activeDir.notes.find(n => n.id === activeNoteId);
            if (note) {
                note.content = currentText;
                note.summary = currentText.substring(0, 30) + '...';
            }
        } else {
            const newNote = { id: Date.now(), content: currentText, summary: currentText.substring(0, 30) + '...' };
            activeDir.notes.push(newNote);
            activeNoteId = newNote.id;
        }
        
        renderDirectoriesAndNotes();
        return true;
    }

    saveNoteBtn.addEventListener('click', () => {
        if (saveOrUpdateCurrentNote()) {
            saveNoteBtn.textContent = 'Salvo!';
            setTimeout(() => { saveNoteBtn.textContent = 'Salvar'; }, 1500);
        }
    });

    newNoteBtn.addEventListener('click', () => {
        saveOrUpdateCurrentNote();
        mainEditor.value = '';
        activeNoteId = null;
        mainEditor.focus();
        renderDirectoriesAndNotes();
    });

    function renderDirectoriesAndNotes() {
        directoryList.innerHTML = '';
        if (directories.length === 0) return directoryList.innerHTML = '<p>Crie uma pasta para começar.</p>';

        directories.forEach(dir => {
            const dirElement = document.createElement('div');
            dirElement.className = 'directory-item';

            const dirHeader = document.createElement('div');
            dirHeader.className = 'directory-header';
            dirHeader.textContent = dir.name;
            if (dir.id === activeDirectoryId) dirHeader.classList.add('active');
            
            dirHeader.addEventListener('click', () => {
                activeDirectoryId = dir.id;
                activeNoteId = null;
                mainEditor.value = '';
                renderDirectoriesAndNotes();
            });

            const notesContainer = document.createElement('div');
            notesContainer.className = 'notes-list-inner';
            
            dir.notes.forEach(note => {
                const noteElement = document.createElement('div');
                noteElement.className = 'note-item';
                noteElement.textContent = note.summary;
                if (note.id === activeNoteId) noteElement.classList.add('active');

                noteElement.addEventListener('click', () => {
                    mainEditor.value = note.content;
                    activeNoteId = note.id;
                    activeDirectoryId = dir.id;
                    renderDirectoriesAndNotes();
                });
                notesContainer.appendChild(noteElement);
            });

            dirElement.appendChild(dirHeader);
            dirElement.appendChild(notesContainer);
            directoryList.appendChild(dirElement);
        });
    }

    // --- LÓGICA DE UPLOAD DE ARQUIVO (CORRIGIDA) ---
    if (fileInput) {
        fileInput.accept = ".pdf,.docx,.txt,.jpg,.jpeg,.png";
        fileInput.addEventListener('change', arquivoSelecionado);
    }

    function arquivoSelecionado() {
        previewArea.innerHTML = ""; // Limpa a área de preview
        if (fileInput.files.length > 0) {
            const arquivo = fileInput.files[0];
            fileNameSpan.textContent = `Arquivo "${arquivo.name}" carregado.`;
            
            const reader = new FileReader();
            
            if (arquivo.type.startsWith("image/")) {
                reader.onload = function(e) {
                    const img = document.createElement("img");
                    img.src = e.target.result;
                    img.style.maxWidth = "100%";
                    img.style.maxHeight = "400px";
                    img.style.display = "block";
                    previewArea.appendChild(img);
                };
                reader.readAsDataURL(arquivo);
            } else if (arquivo.type === "application/pdf") {
                const embed = document.createElement("embed");
                embed.src = URL.createObjectURL(arquivo);
                embed.type = "application/pdf";
                embed.style.width = "100%";
                embed.style.height = "500px";
                previewArea.appendChild(embed);
            } else if (arquivo.type === "text/plain") {
                reader.onload = function(e) {
                    const text = document.createElement("pre");
                    text.textContent = e.target.result;
                    text.style.whiteSpace = "pre-wrap";
                    text.style.wordBreak = "break-all";
                    previewArea.appendChild(text);
                };
                reader.readAsText(arquivo);
            } else {
                previewArea.innerHTML = "<p>Visualização não disponível para este tipo de arquivo.</p>";
            }
        } else {
            fileNameSpan.textContent = "Nenhum arquivo selecionado";
            previewArea.innerHTML = "<p>Nenhum arquivo para visualizar.</p>";
        }
    }
});

