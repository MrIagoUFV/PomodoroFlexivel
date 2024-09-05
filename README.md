# Widget Pomodoro Flexível

Um aplicativo de desktop simples e eficaz para gerenciamento de tempo usando a técnica Pomodoro.

![image](https://github.com/user-attachments/assets/0decf9a2-3162-40f0-9f4a-fbee2a9c9245)


## Características

- Widget flutuante sempre visível
- Controles intuitivos para gerenciar o timer
- Seleção rápida de intervalos de tempo predefinidos
- Alternância entre modos de foco e descanso
- Notificações sonoras e visuais
- Ícone na bandeja do sistema para fácil acesso

## Uso

1. Baixe o arquivo executável "Pomodoro Timer.exe" da seção de releases.

2. Execute o aplicativo clicando duas vezes no arquivo baixado.

3. Use o widget flutuante para controlar o timer:
   - Clique em "▶" para iniciar/pausar o timer
   - Use "+" e "-" para ajustar o tempo
   - Clique no tempo exibido para selecionar intervalos predefinidos
   - Use "M" para alternar entre modos de foco e descanso
   - Clique em "■" para parar e reiniciar o timer
   - Clique em "❌" para fechar o widget (o aplicativo continuará rodando na bandeja do sistema)

4. O aplicativo ficará na bandeja do sistema. Clique com o botão direito no ícone para sair completamente.

## Para desenvolvedores

Se você deseja modificar o código-fonte ou criar seu próprio executável, siga estas instruções:

1. Clone este repositório:
   ````
   git clone https://github.com/seu-usuario/pomodoro-timer.git
   cd pomodoro-timer
   ```

2. Instale as dependências:
   ````
   pip install -r requirements.txt
   ```

3. Para criar o executável:
   ````
   python build.py
   ```

O executável será gerado na pasta `dist`.

## Estrutura do Projeto

