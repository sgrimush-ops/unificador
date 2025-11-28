import pyautogui as pag
import time as t

t.sleep(2)  # Wait for 2 seconds before starting

largura, altura = pag.size()  # Get the screen size
print(f"Largura: {largura}, Altura: {altura}")
pag.moveTo(largura / 2, altura / 2, duration=1)  # Move to the center of the screen
print("Movido para o centro da tela")
pag.moveTo(100, 100, duration=1)  # Move to coordinates (100, 100)
print("Movido para as coordenadas (100, 100)")
pag.moveRel(200, 0, duration=1)  # Move right by 200 pixels
print("Movido 200 pixels para a direita")
pag.moveRel(0, 200, duration=1)  # Move down by 200 pixels
print("Movido 200 pixels para baixo")
pag.moveRel(-200, 0, duration=1)  # Move left by 200 pixels
print("Movido 200 pixels para a esquerda")
pag.moveRel(0, -200, duration=1)  # Move up by
print("Movido 200 pixels para cima")
