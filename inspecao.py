# roda uma vez só — pode deletar depois
from coletor import buscar_pagina

html = buscar_pagina()

with open("html_inspecao.txt", "w", encoding="utf-8") as f:
    f.write(html)

print("Arquivo html_inspecao.txt salvo!")
print("Tamanho:", len(html), "chars")