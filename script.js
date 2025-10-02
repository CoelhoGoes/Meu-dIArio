document.addEventListener('DOMContentLoaded', () => {

    // --- Seletores de Elementos ---
    // Login
    const loginContainer = document.getElementById('login-container');
    const loginForm = document.getElementById('login-form');
    const loginEmailInput = document.getElementById('login-email');
    const loginPasswordInput = document.getElementById('login-password');
    const loginButton = document.getElementById('login-button');
    const loginError = document.getElementById('login-error');
    
    // Wrapper da Aplicação
    const appWrapper = document.getElementById('app-wrapper');

    // Painel da IA
    const openAiPanelButton = document.getElementById('open-ai-panel-btn');
    const aiPanel = document.getElementById('ai-panel');
    const closeAiPanelButton = document.getElementById('close-ai-panel-btn');
    const submitPromptButton = document.getElementById('submit-ai-prompt');
    const promptInput = document.getElementById('ai-prompt-input');
    const responseContent = document.getElementById('ai-response-content');

    // Upload de Arquivo
    const fileInput = document.getElementById('fileInput');
    const fileNameSpan = document.getElementById('fileName');
    const previewArea = document.getElementById('previewArea');


    // --- LÓGICA DE LOGIN ---
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página
        const email = loginEmailInput.value;
        const password = loginPasswordInput.value;
        loginError.textContent = '';
        loginButton.disabled = true;
        loginButton.textContent = 'Verificando...';

        try {
            // ---- SIMULAÇÃO DA REQUISIÇÃO PARA A API DE LOGIN ----
            // !!!! ATENÇÃO: Substitua este bloco pelo 'fetch' real para sua API !!!!
            
            // Exemplo de como seria a requisição POST real:
            /*
            const response = await fetch('https://sua-api.com/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: password })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Usuário ou senha inválidos');
            }

            const userData = await response.json();
            // Aqui você poderia salvar um token de autenticação, etc.
            */

            // Para fins de demonstração, vamos simular uma resposta bem-sucedida.
            // Remova esta simulação quando for conectar com a API real.
            await new Promise((resolve, reject) => {
                setTimeout(() => {
                    if (email === "teste@email.com" && password === "123") {
                        resolve();
                    } else {
                        reject(new Error('Usuário ou senha inválidos'));
                    }
                }, 1000);
            }); 
            
            console.log('Login bem-sucedido (simulado)');
            
            // Se o login for bem-sucedido:
            loginContainer.classList.add('hidden'); // Esconde a tela de login
            appWrapper.classList.remove('hidden'); // Mostra o conteúdo da aplicação

        } catch (error) {
            loginError.textContent = error.message;
        
        } finally {
            loginButton.disabled = false;
            loginButton.textContent = 'Entrar';
        }
    });


    // --- Lógica do Painel da IA (Abrir/Fechar) ---
    openAiPanelButton.addEventListener('click', () => {
        aiPanel.classList.remove('closed');
    });

    closeAiPanelButton.addEventListener('click', () => {
        aiPanel.classList.add('closed');
    });

    // --- Lógica de Envio do Prompt (sem alterações) ---
    submitPromptButton.addEventListener('click', async () => {
        const promptText = promptInput.value;
        if (promptText.trim() === '') {
            alert('Por favor, digite algo para a IA.');
            return;
        }
        submitPromptButton.disabled = true;
        submitPromptButton.textContent = 'Pensando...';
        responseContent.textContent = 'Aguarde, a IA está processando sua solicitação...';
        try {
            const apiUrl = 'https://sua-api-de-ia.com/endpoint';
            const encodedPrompt = encodeURIComponent(promptText);
            const requestUrl = `${apiUrl}?prompt=${encodedPrompt}`;
            const response = await fetch(requestUrl);
            if (!response.ok) {
                throw new Error(`Erro na API: ${response.status}`);
            }
            const data = await response.json();
            responseContent.textContent = data.answer || 'A API não retornou uma resposta válida.';
        } catch (error) {
            console.error('Falha ao buscar resposta da IA:', error);
            responseContent.textContent = 'Desculpe, não foi possível obter uma resposta. Tente novamente.';
        } finally {
            submitPromptButton.disabled = false;
            submitPromptButton.textContent = 'Enviar';
        }
    });

    // --- Lógica de Upload de Arquivo (sem alterações) ---
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
            } else if (arquivo.type === "application/pdf") {
                const embed = document.createElement("embed");
                embed.src = URL.createObjectURL(arquivo);
                embed.type = "application/pdf";
                embed.width = "100%";
                embed.height = "800px";
                previewArea.appendChild(embed);
                adicionarBotaoSalvar();
            } else if (arquivo.type === "text/plain") {
                reader.onload = function(e) {
                    const text = document.createElement("pre");
                    text.textContent = e.target.result;
                    previewArea.appendChild(text);
                    adicionarBotaoSalvar();
                };
                reader.readAsText(arquivo);
            } else {
                previewArea.innerHTML = "<p>Visualização não disponível para este tipo de arquivo.</p>";
                adicionarBotaoSalvar();
            }
        } else {
            fileNameSpan.textContent = "Nenhum arquivo selecionado";
            previewArea.innerHTML = "<p>Nenhum arquivo para visualizar.</p>";
        }
    }
});

