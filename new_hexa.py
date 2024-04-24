import streamlit as st
from polymino import Grid,generate_polyminoes,generate_polymino_positions,unique_grids
from dlx import DLX
from hexa_rotation_flip import P1,P2,P3,P4,P5,P6,P7,P8
from itertools import product
from svgwrite import Drawing,text
import numpy as np  

st.title("Shatkon Paheli")

def solutions_svg(solutions, filename, columns=1, size=5, padding=10,
                  colour=lambda _: "white",stroke_colour="black",
                  stroke_width=10, empty=' '):
    """Format polyomino tilings as an SVG image.

    Args:
        solutions (list): List of polyomino solution grids.
        filename (str): Filename for the SVG image.
        columns (int, optional): Number of columns in the image (Default: 1).
        size (int, optional): Size of each hexagon (default: 25).
        padding (int, optional): Padding around the image (default: 5)
        colour (function, optional): Function taking a piece name and returning its colour (Default: a function returning white for each piece).
        stroke_colour (str, optional): Stroke colour (default: black).
        stroke_width (int, optional): Width of strokes between pieces (default: 3).
        empty (str, optional): String for empty grid point.
    """
    solutions = list(solutions)

    height, width = solutions[0].size

    rows = (len(solutions) + columns - 1) // columns

    drawing_size = (2 * padding + (columns * (3/2 * size) - 0.5) * width,
                    2 * padding + (rows * (np.sqrt(3) * size) - 0.5) * height)

    drawing = Drawing(debug=False, filename=filename, size=drawing_size)
    for i, solution in enumerate(solutions):
        y, x = divmod(i, columns)
        oj = padding + (x * (3/2 * size) - 0.5) * width
        oi = padding + (y * (np.sqrt(3) * size) - 0.5) * height
        group = drawing.g(stroke=stroke_colour, stroke_linecap="round",
                          stroke_width=1)
        drawing.add(group)

        grid = [[empty] * width for _ in range(height)]
        for polymino in solution.polyminoes:
            piece = drawing.g(fill=colour(polymino.name))
            group.add(piece)
            for i, j in polymino.coord:
                x_coord = j * (1.69 * size) + oj + ((i + (j % 8) / 8) * size)
                y_coord = i * (np.sqrt(2) * size) + oi
                # Calculate the points for a pointed top hexagon
                points = [
                    (x_coord + size * np.cos(np.radians(angle)),
                     y_coord + size * np.sin(np.radians(angle)))
                    for angle in range(30, 360, 60)
                ]
                piece.add(drawing.polygon(points))


        # # put in "empty" pieces
        num=1
        for i, j in solution.coord:
            if grid[i][j] == empty:
                x_coord = j * (1.69 * size) + oj + ((i + (j % 8) / 8) * size)
                y_coord = i * (np.sqrt(2.2) * size) + oi
                if number==num:
                    text_element = text.Text(num+1, insert=(x_coord,y_coord), fill='black', font_size=3)
                    num+=2
                else:
                    text_element = text.Text(num, insert=(x_coord,y_coord), fill='black', font_size=3)
                    num+=1
                drawing.add(text_element)

        edges = drawing.path(stroke_width=stroke_width)
        group.add(edges)
        for i, j in product(range(height + 1), range(width)):
            if ((empty if i == 0 else grid[i-1][j])
                != (empty if i == height else grid[i][j])):
                x_coord = j * (3/2 * size) + oj + ((i + (j % 2) / 2) * size)
                y_coord = i * (np.sqrt(3) * size) + oi
                edges.push(['M', x_coord + size * np.cos(np.radians(30)),
                            y_coord + size * np.sin(np.radians(30)),
                            'l', size * np.cos(np.radians(30)),
                            -size * np.sin(np.radians(30))])
        for i, j in product(range(height), range(width + 1)):
            if ((empty if j == 0 else grid[i][j-1])
                != (empty if j == width else grid[i][j])):
                x_coord = j * (3/2 * size) + oj + ((i + (j % 2) / 2) * size)
                y_coord = i * (np.sqrt(3) * size) + oi
                edges.push(['M', x_coord, y_coord, 'l', 0, size])

    drawing.save()

number = st.selectbox("Select a Date", options=list(range(1, 32)), index=0)
if number==26:
    st.write("OOPS!! NO SOLUTION FOUND")
else:
    date_map={
        1:(0,2),
        2:(0,3),
        3:(0,4),
        4:(0,5),
        5:(0,6),
        6:(0,7),
        7:(1,2),
        8:(1,3),
        9:(1,4),
        10:(1,5),
        11:(1,6),
        12:(1,7),
        13:(2,1),
        14:(2,2),
        15:(2,3),
        16:(2,4),
        17:(2,5),
        18:(2,6),
        19:(2,7),
        20:(3,1),
        21:(3,2),
        22:(3,3),
        23:(3,4),
        24:(3,5),
        25:(3,6),
        26:(4,0),
        27:(4,1),
        28:(4,2),
        29:(4,3),
        30:(4,4),
        31:(4,5)
    }
    date_row_col=date_map[number]

    def sortkey(x):
        x = str(x)
        return (len(x), x)

    COLOURS = dict(I="#f15bb5", F="#9b5de5", L="#00bbf9",
                P="#c7ffff", N="#7aff60", T="#e8fa42",
                U="#fb8f23", V="#f44a4a", W="#AAAAEE",
                X="#BB99DD", Y="#CC88CC", Z="#DD99BB")
    GRID = Grid((5, 8), holes=[(0, 0), (1, 0), (2, 0), (3, 0), (0,1), (1,1), (4,6), (3,7), (4,7),date_row_col])
    print(GRID)
    main_polyminoes=[]

    pieces=[P1,P2,P3,P4,P5,P6,P7,P8]
    shade=['I','F','L','P','N','T','U','V','W','X','Y','Z']

    all_solutions = []  
    j=0

    for SHAPES in pieces:
        polyminoes=[]
        for piece in generate_polyminoes(SHAPES):
            for position in generate_polymino_positions(piece, GRID):
                if position not in polyminoes:
                    polyminoes.append(position)
        polyminoes = [polymino.aslist for polymino in polyminoes]
        polyminoes = [list(reversed(inner_list)) for inner_list in polyminoes]
        for i in polyminoes:
            i.pop()
            i.append(shade[j])
        j+=1
        polyminoes = [list(reversed(inner_list)) for inner_list in polyminoes]
        # print("polyminoes",polyminoes)
        main_polyminoes+=polyminoes

    LABELS = list(set([element for polymino in main_polyminoes for element in polymino]))
    LABELS = sorted(LABELS, key=sortkey)

    # print("Grid\n\n",GRID)
    # print("labels\n\n",LABELS)
    # print("poly\n\n",main_polyminoes)

    COVER = DLX(LABELS, main_polyminoes)
    for i, SOLUTION in enumerate(COVER.generate_solutions()):
        solution_grid = Grid.from_DLX(SOLUTION)
        # print(solution_grid)
        all_solutions.append(solution_grid)
        break
    # print(all_solutions)

    solutions_svg([all_solutions[0]], filename='first_solution.svg', columns=7,colour=COLOURS.get)
    svg_content = open("first_solution.svg", "r").read()
    st.write(f"solution for DATE: {number}")
    st.image(svg_content, width=2000)



