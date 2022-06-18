import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #permite pegar um gráfico de plt e colocar no sg
import pandas as pd

# Melhorias: -Quando vou armazenar as variáveis no dataframe(pandas), em arr = pd.read_csv(values['-file_path-'], sep=' ', header=0, names=['eixox', 'eixoy'])
#               eu coloco header=0 e names, que faz ele ignorar a primeira linha, QUE TEM QUE SER CABEÇALHO
#               e atribui nomes pré-definidos pra cada coluna. Seria legal pegar o nome que vem do cabeçalho do arquivo, ou identificar
#               se tem ou não cabeçalho (acho que fazer igual do excel, que vc seleciona se tem ou n seria legal)
#            -Aparentemente, para ter uma janela com scroll é preciso tacar o layout todo em uma coluna... mas fica meio estranho a distância do scroll
#               seria legal melhorar isso (usando um size do column da largura maior q o da window faz isso, mas os elementos ficam não centralizados)
#

def create_plot(x=0, y=0, title='', xlabel='', ylabel='', lcolor='Padrão', grid=False):
    if lcolor == 'Azul':
        lcolor = 'b'
    elif lcolor == 'Verde':
        lcolor = 'g'
    elif lcolor == 'Vermelho':
        lcolor = 'r'
    elif lcolor == 'Ciano':
        lcolor = 'c'
    elif lcolor == 'Magenta':
        lcolor = 'm'
    elif lcolor == 'Amarelo':
        lcolor = 'y'
    elif lcolor == 'Preto':
        lcolor = 'k' 

    if lcolor == 'Padrão':
        plt.plot(x, y)
    else:
        plt.plot(x, y, color=lcolor)

    if grid == True:
        plt.grid(grid)
    plt.title(title, fontsize=18)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    return plt.gcf() #transforma o plot num figure

def delete_plot(canvas):
    canvas.get_tk_widget().forget()
    plt.close('all')    

column_layout = [
        [sg.Text('Gerador de Plots')],
        [sg.Text('Link do arquivo: '), sg.Text(), sg.FileBrowse(button_text='Localizar arquivo', tooltip='Seu arquivo deve conter cabeçalho!', key='-file_path-', file_types=(("Text Files", "*.txt"),)), sg.Push(), sg.Button(button_text='Gerar Plot',key='-plot-')], #segundo a documentação, o filetypes TEM que ter aquela virgula após o tipo de arquivo dado
        [sg.Canvas(size=(100, 100), key='-CANVAS-')],
        [sg.Text('Título do gráfico: '), sg.InputText(key='-title-', size=(30,1)), sg.Text('Label eixo x: '), sg.InputText(key='-xlabel-', size=(20, 1)), sg.Text('Label eixo y: '), sg.InputText(key='-ylabel-', size=(20, 1))], # na documentação do sg, o cara sugere que toda key que retornar string esteja entre hífens
        [sg.Text('Cor do traçado'), sg.Combo(['Padrão', 'Azul', 'Verde', 'Vermelho', 'Ciano', 'Magenta', 'Amarelo', 'Preto'], key='-color-', default_value='Padrão', readonly=True), sg.Text('Grid'), sg.Checkbox('',key='-grid-')],
        [sg.Button(button_text='Aplicar mudanças', key='-apply-')],
        [sg.Exit()]
        ]

layout = [[sg.Column(column_layout, element_justification='c', scrollable=True, vertical_scroll_only=True, size=(1250,700), size_subsample_height=1, size_subsample_width=0.9)]] # a documentação avisa que o size não funciona muito bem

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw() #desenha o plot no canvas
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

window = sg.Window("Gerador de Plots", layout, size=(900,800), finalize=True, element_justification='c', location=(150,0), margins=(20,20), resizable=True) # finalize=True é para fazer canvas funcionar usando tkinter 
titulo = 'Título'
xlabel = 'Eixo x'
ylabel = 'Eixo y'
graf = create_plot(0, 0, titulo, xlabel, ylabel)

canvas = draw_figure(window['-CANVAS-'].TKCanvas, graf)

while True: # loop para processar os eventos e pegar os valores dos inputs
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': #Sempre colocar após o window.read()
        break

    elif event == '-plot-':
        try:
            if graf is not None:
                delete_plot(canvas)
                arr = pd.read_csv(values['-file_path-'], sep=' ', header=0, names=['eixox', 'eixoy'])
                graf = create_plot(arr.eixox, arr.eixoy, titulo, xlabel, ylabel, values['-color-'], values['-grid-'])
                canvas = draw_figure(window['-CANVAS-'].TKCanvas, graf)
                window.refresh()
        except:
            canvas = draw_figure(window['-CANVAS-'].TKCanvas, graf) #pra ficar visualmente melhor, pois se não colocar, o canvas some
            sg.popup('Caminho Inválido!!!')

    elif event == '-apply-':
        try:
            if graf is not None:
                delete_plot(canvas) #se não apaga o canvas, ele continua gerando plot um embaixo do outro
                arr = pd.read_csv(values['-file_path-'], sep=' ', header=0, names=['eixox', 'eixoy'])
                if values['-title-']!='':
                    titulo = values['-title-']
                    xlabel = values['-xlabel-']
                    ylabel = values['-ylabel-']
                graf = create_plot(arr.eixox, arr.eixoy, titulo, xlabel, ylabel, values['-color-'], values['-grid-'])
                canvas = draw_figure(window['-CANVAS-'].TKCanvas, graf)
                window.refresh()
        except:
            if values['-title-']!='':
                    titulo = values['-title-']
                    xlabel = values['-xlabel-']
                    ylabel = values['-ylabel-']
            graf = create_plot(0, 0, titulo, xlabel, ylabel, values['-color-'], values['-grid-'])
            canvas = draw_figure(window['-CANVAS-'].TKCanvas, graf)
            window.refresh()
            sg.popup('Caminho Inválido!!!')
            
window.close()