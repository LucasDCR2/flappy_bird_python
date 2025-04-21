# 🐦 Flappy Bird com OpenGL em Python

Este projeto é uma implementação do clássico jogo **Flappy Bird** utilizando **OpenGL** com **Python**, desenvolvido como trabalho da disciplina de **Computação Gráfica** na **UNISC**, sob orientação do professor **Rafael**.

## 🚀 Funcionalidades

- ✅ Renderização 2D com PyOpenGL
- ✅ Controle de eventos com GLFW (teclado e mouse)
- ✅ Gerenciamento de texturas com Pillow
- ✅ Sistema de colisão entre pássaro, canos e chão
- ✅ Pontuação progressiva e sistema de vidas (3 vidas por partida)
- ✅ Aumento de dificuldade a cada 5 pontos (velocidade e spawn dos canos)
- ✅ Overlays de Início e Fim de jogo com botões interativos
- ✅ Arquitetura modular e organizada

---

## 📦 Bibliotecas Utilizadas

| Biblioteca | Finalidade |
|-----------|------------|
| `glfw` | Criação da janela e captura de eventos do teclado/mouse |
| `PyOpenGL` | Renderização gráfica 2D com OpenGL |
| `Pillow` | Manipulação e carregamento de texturas (sprites) |
| `time` | Cálculo do delta time e controle de tempo |
| `numpy` e `random` | Utilizadas em módulos auxiliares (ex: canos aleatórios) |

---
## 🎮 Controles

- **Espaço** ou **Clique do Mouse** – Pular
- **R** – Reiniciar (se estiver no Game Over)
- **Esc** – Fechar o jogo

---

## 💡 Como Funciona o Código (main.py)

- A função `initialize()` prepara a janela GLFW, carrega texturas, e configura a projeção ortográfica.
- O loop principal do jogo é executado dentro de `main()`, onde:
  - `update()` atualiza a lógica do jogo (movimentos, colisões, pontuação)
  - `render()` desenha todos os elementos na tela com a ordem correta
- A colisão é verificada em `check_collisions()`:
  - Ao colidir, o jogador perde uma vida. Com 0 vidas, aparece o Game Over.
  - Caso tenha vidas restantes, o jogo reinicia automaticamente.
- A dificuldade aumenta automaticamente conforme a pontuação.
